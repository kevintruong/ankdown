import os

import i18n

cur_dir = os.path.dirname(__file__)
i18n.set("filename_format", "{locale}.{format}")
i18n.set("skip_locale_root_data", True)
i18n.set("locale", "English")
i18n.set("fallback", "English")
i18n.load_path.append(os.path.join(cur_dir, "../assets/"))

#    "Persian",
supported_languages = [
    "English"
]
