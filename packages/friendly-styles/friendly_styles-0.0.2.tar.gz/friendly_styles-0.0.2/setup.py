from setuptools import setup

setup(
    entry_points={
        "pygments.styles": [
            "friendly_light = styles.friendly_light:FriendlyLightStyle",
            "friendly_dark = styles.friendly_dark:FriendlyDarkStyle",
        ]
    }
)
