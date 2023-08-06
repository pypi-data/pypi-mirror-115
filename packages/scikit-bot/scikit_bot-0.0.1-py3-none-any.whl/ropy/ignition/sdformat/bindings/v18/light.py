from dataclasses import dataclass, field
from typing import Optional

__NAMESPACE__ = "sdformat/v1.8/light.xsd"


@dataclass
class Light:
    """
    The light element describes a light source.

    Parameters
    ----------
    cast_shadows: When true, the light will cast shadows.
    intensity: Scale factor to set the relative power of a light.
    diffuse: Diffuse light color
    specular: Specular light color
    attenuation: Light attenuation
    direction: Direction of the light, only applicable for spot and
        directional lights.
    spot: Spot light parameters
    pose: A position(x,y,z) and orientation(roll, pitch yaw) with
        respect to the frame named in the relative_to attribute.
    name: A unique name for the light.
    type: The light type: point, directional, spot.
    """

    class Meta:
        name = "light"

    cast_shadows: bool = field(
        default=False,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    intensity: float = field(
        default=1.0,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    diffuse: str = field(
        default="1 1 1 1",
        metadata={
            "type": "Element",
            "namespace": "",
            "pattern": r"(\s*\+?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+)\s+){3}\+?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+)\s*",
        },
    )
    specular: str = field(
        default=".1 .1 .1 1",
        metadata={
            "type": "Element",
            "namespace": "",
            "pattern": r"(\s*\+?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+)\s+){3}\+?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+)\s*",
        },
    )
    attenuation: Optional["Light.Attenuation"] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    direction: str = field(
        default="0 0 -1",
        metadata={
            "type": "Element",
            "namespace": "",
            "pattern": r"(\s*(-|\+)?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+)\s+){2}((-|\+)?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+))\s*",
        },
    )
    spot: Optional["Light.Spot"] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    pose: "Light.Pose" = field(
        default="0 0 0 0 0 0",
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    type: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )

    @dataclass
    class Attenuation:
        """
        Light attenuation.

        Parameters
        ----------
        range: Range of the light
        linear: The linear attenuation factor: 1 means attenuate evenly
            over the distance.
        constant: The constant attenuation factor: 1.0 means never
            attenuate, 0.0 is complete attenutation.
        quadratic: The quadratic attenuation factor: adds a curvature to
            the attenuation.
        """

        range: float = field(
            default=10.0,
            metadata={
                "type": "Element",
                "namespace": "",
            },
        )
        linear: float = field(
            default=1.0,
            metadata={
                "type": "Element",
                "namespace": "",
            },
        )
        constant: float = field(
            default=1.0,
            metadata={
                "type": "Element",
                "namespace": "",
            },
        )
        quadratic: float = field(
            default=0.0,
            metadata={
                "type": "Element",
                "namespace": "",
            },
        )

    @dataclass
    class Spot:
        """
        Spot light parameters.

        Parameters
        ----------
        inner_angle: Angle covered by the bright inner cone
        outer_angle: Angle covered by the outer cone
        falloff: The rate of falloff between the inner and outer cones.
            1.0 means a linear falloff, less means slower falloff,
            higher means faster falloff.
        """

        inner_angle: float = field(
            default=0.0,
            metadata={
                "type": "Element",
                "namespace": "",
            },
        )
        outer_angle: float = field(
            default=0.0,
            metadata={
                "type": "Element",
                "namespace": "",
            },
        )
        falloff: float = field(
            default=0.0,
            metadata={
                "type": "Element",
                "namespace": "",
            },
        )

    @dataclass
    class Pose:
        """
        Parameters
        ----------
        value:
        relative_to: Name of frame relative to which the pose is
            applied.
        """

        value: Optional[str] = field(
            default=None,
            metadata={
                "required": True,
                "pattern": r"(\s*(-|\+)?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+)\s+){5}((-|\+)?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+))\s*",
            },
        )
        relative_to: Optional[str] = field(
            default=None,
            metadata={
                "type": "Attribute",
            },
        )
