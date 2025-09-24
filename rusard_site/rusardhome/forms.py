from django import forms


class ContactForm(forms.Form):
    firstname = forms.CharField(
        label="Prénom",
        max_length=150,
    )
    name = forms.CharField(
        label="Nom",
        max_length=150,
    )
    email = forms.EmailField(
        label="Email",
        max_length=254,
    )
    message = forms.CharField(
        label="Message",
        widget=forms.Textarea,
        max_length=2000,
    )
    website = forms.CharField(
        required=False,
        label="Site web",
        widget=forms.TextInput,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name != "website":
                classes = field.widget.attrs.get("class", "")
                field.widget.attrs["class"] = f"form-control {classes}".strip()
            if field_name == "message":
                field.widget.attrs.setdefault("rows", 4)

        # Honeypot should remain invisible but accessible to screen readers
        website_widget = self.fields["website"].widget
        website_widget.attrs.setdefault("autocomplete", "off")
        website_widget.attrs.setdefault("tabindex", "-1")
        website_widget.attrs.setdefault("aria-hidden", "true")

    def clean_website(self):
        website = self.cleaned_data.get("website", "").strip()
        if website:
            raise forms.ValidationError("Le formulaire n'a pas pu être envoyé.")
        return website
