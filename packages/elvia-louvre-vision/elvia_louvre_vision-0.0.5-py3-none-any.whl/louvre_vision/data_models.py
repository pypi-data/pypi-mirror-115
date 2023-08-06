from azure.cognitiveservices.vision.customvision.training.models import ImageFileCreateEntry, ImageUrlCreateEntry, Region, Tag
from dataclasses import dataclass
from elvia_louvre.louvre_client import LouvreClient
from elvia_louvre.data_models import ImageData
from typing import Dict, List, Set, Tuple, Union

from louvre_vision.config import Config
from louvre_vision.errors import LouvreVisionValueError
from louvre_vision.images import ImageMethods
from louvre_vision.methods import Methods


@dataclass
class TrainingImage:

    identifier: str

    def __lt__(self, other):
        """Lower-than operator, used when sorting lists of instances of this class."""
        return self.identifier < other.identifier

    def __hash__(self):
        return hash(self.identifier)

    def __eq__(self, other):
        return self.__hash__() == other.__hash__()

    @staticmethod
    def get_tag_id(label: str, tags: List[Tag]) -> str:
        """
        Given an image label or region tag, return the corresponding tag id.
        
        :param str label: Name of the label or category for which the tag id is desired.
        :param list tags: List of Tag objects, coming from the Custom Vision SDK, that represent existing tags in a Custom Vision project.
        :rtype: str
        :raises LouvreVisionValueError:
        """

        tag_id = next((tag.id for tag in tags if tag.name == label), None)
        if tag_id is None:
            raise LouvreVisionValueError(
                f'No tag.id found for tag name: {label}')

        return tag_id

    def get_imagecreateentry(
        self,
        tags: List[Tag],
        louvre_client: LouvreClient,
        using_production_images: bool = True
    ) -> Union[ImageUrlCreateEntry, ImageFileCreateEntry, None]:

        raise NotImplementedError()

    @staticmethod
    def _create_imagecreateentry_from_url(
        image_url: str,
        tag_ids: List[str] = [],
        regions: List[Region] = []
    ) -> Union[ImageUrlCreateEntry, ImageFileCreateEntry]:

        file_size = Methods.get_remote_file_size(file_url=image_url)

        return ImageUrlCreateEntry(
            url=image_url, tag_ids=tag_ids, regions=regions
        ) if file_size and file_size < Config.custom_vision_max_training_file_size else ImageFileCreateEntry(
            name=Methods.extract_filename(file_path=image_url),
            contents=ImageMethods.resize_from_url(
                image_url=image_url,
                image_longer_side=Config.image_longer_side),
            tag_ids=tag_ids,
            regions=regions)

    @staticmethod
    def _create_imagecreateentry_from_image_data(
        image_data: ImageData,
        tag_ids: List[str] = [],
        regions: List[Region] = [],
    ) -> Union[ImageUrlCreateEntry, ImageFileCreateEntry, None]:

        image_entry = ImageMethods.get_image_from_image_data(
            image_data=image_data,
            max_file_size=Config.custom_vision_max_training_file_size)

        if image_entry.is_empty:
            return None

        # image_payload is either a sasuri string or bytes
        if image_entry.sasuri:
            return ImageUrlCreateEntry(url=image_entry.sasuri,
                                       tag_ids=tag_ids,
                                       regions=regions)
        # image_payload is bytes
        image_variant = image_data.get_variant(
            ImageMethods.select_preferred_image_variant_for_custom_vision(
                image_data=image_data))
        file_name = Methods.extract_filename(
            file_path=image_variant.sasuri
        ) if image_variant else image_data.image_id
        return ImageFileCreateEntry(name=file_name,
                                    contents=image_entry.file_bytes,
                                    tag_ids=tag_ids,
                                    regions=regions)


@dataclass
class ClassificationTrainingImage(TrainingImage):

    labels: List[str]

    def __hash__(self):
        return hash(self.identifier + str((label for label in self.labels)))

    def get_imagecreateentry(
        self,
        tags: List[Tag],
        louvre_client: LouvreClient,
        using_production_images: bool = True
    ) -> Union[ImageUrlCreateEntry, ImageFileCreateEntry, None]:
        """
        Create an object that represents a training image that can be sent to Custom Vision.

        :param list tags: List of Tag objects representing tags available in a Custom Vision project. 
        :param LouvreClient louvre_client: LouvreClient instance with access to where the current image exists.
        :param bool using_production_images: Whether to use production credentials. Defaults to True.
        :rtype: ImageUrlCreateEntry | ImageFileCreateEntry | None
        :raises LouvreImageNotFound:
        :raises LouvreKeyError:
        :raises LouvreQueryError:
        :raises RequestException:
        """
        image_tag_ids = []
        for label in list(set(self.labels)):
            image_tag_ids.append(super().get_tag_id(label=label, tags=tags))
        if Methods.is_string_url(self.identifier):
            return super()._create_imagecreateentry_from_url(
                image_url=self.identifier, tag_ids=image_tag_ids)
        image_data = louvre_client.get_image_data(
            image_id=self.identifier,
            using_production_images=using_production_images)
        return super()._create_imagecreateentry_from_image_data(
            image_data=image_data, tag_ids=image_tag_ids)


@dataclass
class RegionBoundingBox:

    top: float
    left: float
    width: float
    height: float
    decimal_places: int = Config.predictions_rounding_decimal_places

    def __str__(self) -> str:
        strings = [
            f'top = {str(round(self.top, self.decimal_places))}; ',
            f'left = {str(round(self.left, self.decimal_places))}; ',
            f'width = {str(round(self.width, self.decimal_places))}; ',
            f'height = {str(round(self.height, self.decimal_places))}'
        ]
        return ''.join(strings)

    def __repr__(self) -> str:
        return self.__str__()

    def to_tuple(self, height: int,
                 width: int) -> Tuple[float, float, float, float]:
        """Return as tuple: (left, upper, right, lower)"""
        left = round(self.left * width, self.decimal_places)
        upper = round(self.top * height, self.decimal_places)
        right = round(left + width * self.width, self.decimal_places)
        lower = round(upper + height * self.height, self.decimal_places)

        return (left, upper, right, lower)


@dataclass
class ImageRegion:

    bounding_box: RegionBoundingBox
    tag_name: str

    def to_dict(self) -> dict:
        return {
            'tag_name': self.tag_name,
            'top': self.bounding_box.top,
            'left': self.bounding_box.left,
            'width': self.bounding_box.width,
            'height': self.bounding_box.height
        }


@dataclass
class ObjectDetectionTrainingImage(TrainingImage):

    regions: List[ImageRegion]

    def __hash__(self):
        return hash(self.identifier + str(self.regions))

    @property
    def unique_tags(self) -> Set[str]:
        """
        Return the unique tag names present in the image.
        
        :rtype: set
        """
        return set([region.tag_name for region in self.regions])

    def get_imagecreateentry(
        self,
        tags: List[Tag],
        louvre_client: LouvreClient,
        using_production_images: bool = True
    ) -> Union[ImageUrlCreateEntry, ImageFileCreateEntry, None]:
        """
        Create an object that represents a training image that can be sent to Custom Vision.

        :param list tags: List of Tag objects representing tags available in a Custom Vision project. 
        :param LouvreClient louvre_client: LouvreClient instance with access to where the current image exists.
        :param bool using_production_images: Whether to use production credentials. Defaults to True.
        :rtype: ImageUrlCreateEntry | ImageFileCreateEntry | None
        :raises LouvreImageNotFound:
        :raises LouvreKeyError:
        :raises LouvreQueryError:
        :raises RequestException:
        """
        regions = self._get_custom_vision_regions(tags=tags)
        if Methods.is_string_url(self.identifier):
            return super()._create_imagecreateentry_from_url(
                image_url=self.identifier, regions=regions)
        image_data = louvre_client.get_image_data(
            image_id=self.identifier,
            using_production_images=using_production_images)
        return super()._create_imagecreateentry_from_image_data(
            image_data=image_data, regions=regions)

    def _get_custom_vision_regions(self, tags: List[Tag]) -> List[Region]:
        """
        Return a list of Custom Vision Region objects representing the detected objects.
        The method output can be used in the creation of subsequent ImageXXXXCreateEntry objects.
        """
        regions: List[Region] = []
        for region in self.regions:
            regions.append(
                Region(tag_id=super().get_tag_id(label=region.tag_name,
                                                 tags=tags),
                       left=region.bounding_box.left,
                       top=region.bounding_box.top,
                       width=region.bounding_box.width,
                       height=region.bounding_box.height))

        return regions


@dataclass
class UploadImageEntry:

    image_create_entry: Union[ImageFileCreateEntry, ImageUrlCreateEntry]
    metadata: Dict[str, str]
