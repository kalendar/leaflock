from enum import StrEnum

from bidict import bidict


class License(StrEnum):
    CC0_1_0 = "CC0 1.0"
    CC_BY_4_0 = "CC BY 4.0"
    CC_BY_SA_4_0 = "CC BY-SA 4.0"
    CC_BY_NC_4_0 = "CC BY-NC 4.0"
    CC_BY_NC_SA_4_0 = "CC BY-NC-SA 4.0"


LICENSE_MAP = bidict(
    {
        "CC0 1.0": "CC0 1.0 Universal",
        "CC BY 4.0": "Creative Commons Attribution 4.0 International",
        "CC BY-SA 4.0": "Creative Commons Attribution-ShareAlike 4.0 International",
        "CC BY-NC 4.0": "Creative Commons Attribution-NonCommercial 4.0 International",
        "CC BY-NC-SA 4.0": "Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International",
    }
)
