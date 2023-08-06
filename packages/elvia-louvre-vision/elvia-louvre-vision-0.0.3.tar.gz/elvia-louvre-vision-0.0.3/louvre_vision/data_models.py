from azure.cognitiveservices.vision.customvision.training.models import ImageFileCreateEntry, ImageUrlCreateEntry, Region, Tag  # type: ignore
from dataclasses import dataclass
from elvia_louvre.data_models import ImageData  # type: ignore
from typing import List, Union

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
