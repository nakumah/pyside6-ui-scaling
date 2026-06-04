import os

from dataclasses import dataclass
from resources.colors import AppColors

"""
The goal is to be able to generate

QLabel[variantId="variantIdValue"]{
    variantBodyKey: "variantBodyValue"
}

"""


@dataclass
class Variant:
    widgetName: str  # e.g. QLabel
    variantId: str  # e.g. textColor, fontWeight
    variantIdValue: str  # e.g. danger, light, bold
    variantBodyKey: str  # e.g. color, font-weight
    variantBodyKeyValue: str  # e.g. @danger, light, 2px
    variantObjectName: str  = "" # VDangerLineEdit

    def constructVariantBodyString(self) -> str:
        assert self.variantBodyKey != ""
        assert self.variantBodyKeyValue != ""

        return f"{self.variantBodyKey}: {self.variantBodyKeyValue};"

    def constructVariantTag(self) -> str:
        assert self.variantId != ""
        assert self.variantIdValue != ""

        return f'[{self.variantId}="{self.variantIdValue}"]'

    def constructVariantQSS(self) -> str:
        assert self.widgetName != ""
        objectNameString = f"#{self.variantObjectName}" if len(self.variantObjectName) > 0 else ""
        return f"{self.widgetName}{objectNameString}{self.constructVariantTag()}{{\n\t{self.constructVariantBodyString()}\n}}\n"

    @staticmethod
    def constructMultiTagVariantQSS(
        widgetName: str, tags: list[str], bodyStrings: list[str], objectName: str = ""
    ) -> str:

        body = ""
        for bodyString in bodyStrings:
            body += "\t" + bodyString + "\n"
        fullBody = "{\n" + body + "}\n"

        fullTag = ""
        for tag in tags:
            fullTag += tag

        objectNameString = f"#{objectName}" if len(objectName) > 0 else ""
        
        qss = f"{widgetName}{objectNameString}{fullTag}{fullBody}"
        return qss


@dataclass
class QLabelColorVariant(Variant):
    variantId: str = ""
    variantIdValue: str = ""
    variantBodyKey: str = "color"
    variantBodyKeyValue: str = ""
    widgetName = "QLabel"
    variantObjectName: str = "VLabel"


@dataclass
class QLabelFontWeightVariant(Variant):

    widgetName: str = "QLabel"
    variantId: str = "fontWeight"
    variantIdValue: str = ""
    variantBodyKey: str = "font-weight"
    variantBodyKeyValue: str = ""
    variantObjectName: str = "VLabel"


class VariantGenerator:
    def __init__(self):

        self.colors = self.parseColorClass(AppColors)
        self.fontWeightVariants: list[QLabelFontWeightVariant] = (
            self.createFontWeightVariants()
        )
        self.colorVariants: list[QLabelColorVariant] = self.createColorVariants()

    def createColorVariants(self) -> list[QLabelColorVariant]:
        variants = []

        for colorName, _ in self.colors.items():
            colorVariant = QLabelColorVariant(
                widgetName="QLabel",
                variantId="textColor",
                variantIdValue=colorName,
                variantBodyKey="color",
                variantBodyKeyValue=f"@{colorName}",
            )
            variants.append(colorVariant)

        return variants

    def createFontWeightVariants(self) -> list[QLabelFontWeightVariant]:
        variants = []
        for v in ["light", "bold"]:
            variants.append(
                QLabelFontWeightVariant(
                    variantIdValue=v,
                    variantBodyKeyValue=v,
                )
            )

        return variants

    @staticmethod
    def _generateVariantQSS(variants: list[Variant]):
        qss = ""
        for variant in variants:
            qss += variant.constructVariantQSS() + "\n"
        return qss

    def generateFontWeightVariantQSS(self):
        return self._generateVariantQSS(self.fontWeightVariants)

    def generateColorVariantQSS(self):
        return self._generateVariantQSS(self.colorVariants)

    def generateMixedVariantQSS(self):
        qss = ""

        for colorVariant in self.colorVariants:
            for fwVariant in self.fontWeightVariants:

                tags = [
                    colorVariant.constructVariantTag(),
                    fwVariant.constructVariantTag(),
                ]
                bodies = [
                    colorVariant.constructVariantBodyString(),
                    fwVariant.constructVariantBodyString(),
                ]

                _qss = Variant.constructMultiTagVariantQSS(
                    widgetName=colorVariant.widgetName, tags=tags, bodyStrings=bodies,
                    objectName=fwVariant.variantObjectName
                )

                qss += _qss + "\n"

        return qss

    def parseColorClass(self, colorClass: object):
        colors = {}

        for k, v in vars(colorClass).items():
            if k.startswith("_"):
                continue
            colors[k] = v

        return colors

    def saveToFile(self, file: str, data: str):
        with open(file, "w") as f:
            f.write("/* Generated from qlabel qss */")

        with open(file, "a") as f:
            f.write(data)


gen = VariantGenerator()

qss = "\n"
qss += gen.generateFontWeightVariantQSS()
qss += gen.generateColorVariantQSS()
qss += gen.generateMixedVariantQSS()

qssFile = os.path.join(os.getcwd(), "resources", "qss", "q_label.qss")
gen.saveToFile(qssFile, qss)
