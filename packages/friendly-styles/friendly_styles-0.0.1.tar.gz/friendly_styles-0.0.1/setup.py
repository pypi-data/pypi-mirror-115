from setuptools import setup

setup(
    entry_points={
        "pygments.styles": [
            "friendly_light = friendly_styles.styles.friendly_light:FriendlyLightStyle",
            "friendly_dark = friendly_styles.styles.friendly_dark:FriendlyDarkStyle",
        ]
    }
)
