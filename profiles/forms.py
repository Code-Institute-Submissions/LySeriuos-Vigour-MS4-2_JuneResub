from django import forms
from .models import UserProfile


# Meta options telling django which model it'll be associated with
# and which fields to render.
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = ('user',)

    def __init__(self, *args, **kwargs):
        """Add placeholders and classes, remove auto-generated
        labels and set autofocus on first field"""
        # First call the default init method to set the form up as it would be by default
        super().__init__(*args, **kwargs)
        # dictionary of placeholders which will show up
        # in the form fields
        placeholders = {
            "default_phone_number": "Phone Number",
            "default_postcode": "Postal Code",
            "default_town_or_city": "Town or City",
            "default_street_address1": "Street Address 1",
            "default_street_address2": "Street Address 2",
            "default_county": "County, State or Locality",
        }

        # setting the autofocus attribute on the full name field to true
        # The cursor will start in the full name field when the user loads the page
        self.fields["default_phone_number"].widget.attrs["autofocus"] = True
        # Iterate through the forms fields adding a star to the placeholder
        # if it's a required field on the model
        for field in self.fields:
            # removed placeholder for country gives an error taht missing key. 
            # To fix this error need to make this if statement:
            if field != 'default_country':
                if self.fields[field].required:
                    placeholder = f"{placeholders[field]} *"
                else:
                    placeholder = placeholders[field]
                # Setting all the placeholder attributes to their values in the dictionary above.
                self.fields[field].widget.attrs["placeholder"] = placeholder
            # css class
            self.fields[field].widget.attrs["class"] = "profile-form-input"
            # removing the form fields labels.
            self.fields[field].label = False