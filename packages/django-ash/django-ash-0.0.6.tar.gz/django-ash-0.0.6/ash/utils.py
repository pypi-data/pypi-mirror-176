from django import forms

def substract_media(media1, media2):
    return forms.Media(
        js=list(set(media1._js) - set(media2._js)),
        css={
            key: list(set(media1._css.get(key, [])) - set(media2._css.get(key, [])))
            for key in [*media1._css, *media2._css]
        }
    )