import xml.etree.ElementTree as et
from typing import Dict
import uuid
from abc import ABC, abstractmethod
class Question(ABC):

    def __init__(self, identify_id: str, text: str):
        self.identify_id: str = identify_id
        self.text: str = text
        self.internal_id: str = str(uuid.uuid4())
        self.xml: et.Element = self.instantiate_xml()

    @abstractmethod
    def instantiate_xml(self) -> et.Element:
        pass

    def get_xml(self) -> et.Element:
        """Returns the xml structure of the comment question."""
        return self.xml

    def pretty_print(self) -> str:
        et.indent(self.xml)
        return et.tostring(self.xml).decode()
    
class CommentQuestion(Question):
    """Class to represent a comment question in a questionnaire."""

    def __init__(self, identify_id: str, text: str):
        self.identify_id: str = identify_id
        self.text: str = text
        self.internal_id: str = str(uuid.uuid4())
        self.xml: et.Element = self.instantiate_xml()

    def instantiate_xml(self) -> et.Element:
        """Builds the basic XML structure of the comment question."""
        root = et.Element("commentQuestion")

        # Insert immediate children to the root.
        static_children: Dict[str, str] = {"isPersonalize":"false", "QuestionDisplayType":"All", "ID":self.internal_id, "IdentifyID": self.identify_id}
        for child, value in static_children.items():
            child_xml = et.SubElement(root, child)
            child_xml.text = value
  
        # Build the questionTitle from instance variables.
        question_title_xml = et.SubElement(root, "questionTitle")
        
        caption_xml = et.SubElement(question_title_xml, "caption")
        caption_xml.set("lang", "en-US")
        caption_xml.text = self.text

        caption_id_xml = et.SubElement(caption_xml, "id")
        caption_id_xml.text = f"questionnaire/commentBox/{self.internal_id}/questionTitle@id=en-US"

        return root

class RatingQuestion(Question):
    """Class to represent a comment question in a questionnaire."""

    def __init__(self, identify_id: str, text:str, scales: Dict[str, str], na: str=""):
        self.identify_id: str = identify_id
        self.text: str = text
        self.scales = scales
        self.internal_id: str = str(uuid.uuid4())
        self.na: str = na
        self.xml: et.Element = self.instantiate_xml()
        
    def instantiate_xml(self) -> et.Element:
        """Builds the basic XML structure of the comment question."""
        root = et.Element("ratingQuestion")

        # Insert immediate children to the root.
        static_children: Dict[str, str] = {"isPersonalize":"false", "QuestionDisplayType":"All", "ID":self.internal_id, "IdentifyID":self.identify_id, "isSingleRow":"true"}
        for child, value in static_children.items():
            child_xml = et.SubElement(root, child)
            child_xml.text = value
  
        # Build the questionTitle from instance variables.
        question_title_xml = et.SubElement(root, "questionTitle")
        
        caption_xml = et.SubElement(question_title_xml, "caption")
        caption_xml.set("lang", "en-US")
        caption_xml.text = self.text

        caption_id_xml = et.SubElement(caption_xml, "id")
        caption_id_xml.text = f"questionnaire/ratingQuestion/{self.internal_id}/questionTitle@id=en-US"

        # Build the primaryScale xml.
        primary_scale_xml = et.SubElement(root, "primaryScale")
        display_as_radio_xml = et.SubElement(primary_scale_xml, "displayAsRadioButton")
        display_as_radio_xml.text = "true"

        i: int = 1
        for score, scale in self.scales.items():
            scale_xml = self._build_scale(score, scale, str(i))
            primary_scale_xml.append(scale_xml)
            i += 1

        # Handle the NA value.
        na_scale_xml = self._build_scale("", self.na, str(i))
        primary_scale_xml.append(na_scale_xml)
        
        return root
    
    def _build_scale(self, score: str, scale: str, index: str) -> et.Element:
        scale_xml = et.Element("scale")
        scale_xml.set("mandatory", "true")

        scale_caption_xml = et.SubElement(scale_xml, "caption")
        scale_caption_xml.set("lang", "en-US")

        scale_id = et.SubElement(scale_caption_xml, "id")
        scale_id.text = f"questionnaire/ratingQuestion/{self.internal_id}/scale{index}@id=en-US"
        scale_id.tail = scale

        score_xml = et.SubElement(scale_xml, "score")
        score_xml.text = score

        return scale_xml

class SectionBox:

    def __init__(self, text:str):
        self.text = text
        self.internal_id: str = str(uuid.uuid4())
        self.xml: et.Element = self.instantiate_xml()
    def instantiate_xml(self) -> et.Element:
        root = et.Element("sectionBox")

        # Build Identify ID.
        child_xml = et.SubElement(root, "ID")
        child_xml.text = self.internal_id

        # Build Question Title.
        question_title_xml = et.SubElement(root, "questionTitle")

        caption_xml = et.SubElement(question_title_xml, "caption")
        caption_xml.set("lang", "en-US")
        caption_xml.text = self.text

        caption_id_xml = et.SubElement(caption_xml, "id")
        caption_id_xml.text = f"questionnaire/SectionBox/{self.internal_id}/questionTitle@id=en-US"

        return root

    def get_xml(self) -> et.Element:
        """Returns the xml structure of the comment question."""
        return self.xml
    
    def pretty_print(self) -> str:
        et.indent(self.xml)
        return et.tostring(self.xml).decode()

if __name__ == "__main__":
    test = SectionBox("Test Section Title")
    print(test.pretty_print())