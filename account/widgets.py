from django.forms.widgets import RadioSelect
from django.utils.safestring import mark_safe

class ImageRadioSelect(RadioSelect):
    def render(self, name, value, attrs=None, renderer=None):
        output = []
        for choice_value, choice_label in self.choices:
            icon_url = choice_label  # Choice label contains the image URL
            checked = 'checked' if str(value) == str(choice_value) else ''
            active_class = 'selected' if checked else ''

            output.append(f"""
                <label class="profile-icon-label {active_class}" style="text-align: center; margin: 10px;">
                    <input type="radio" name="{name}" value="{choice_value}" {checked} class="profile-icon-radio" style="display: none;">
                    <img src="{icon_url}" class="profile-icon img-thumbnail" width="100" height="100">
                </label>
            """)
        return mark_safe('<div class="row justify-content-center">' + ''.join(output) + '</div>')
