from test_plus.test import TestCase

from django.core.exceptions import ValidationError

from loki.education.validators import (
    validate_phone,
    validate_mac
)

from loki.seed.factories import faker


class TestValidators(TestCase):
    def test_validate_phone_returns_true_for_valid_phone(self):
        phone = '+359 888 888 888'

        try:
            validate_phone(phone)
        except ValidationError:
            self.fail('Should not raise validation error')

    def test_validate_phone_raises_validation_error_for_invalid_phone(self):
        phones = ['1234', 'asdfasdf']

        for phone in phones:
            with self.assertRaises(ValidationError):
                validate_phone(phone)

    def test_validate_mac_returns_true_for_valid_mac(self):
        mac = faker.mac_address()

        try:
            validate_mac(mac)
        except ValidationError:
            self.fail('Should not raise validation error')

    def test_validate_mac_raises_validation_error_for_invalid_mac(self):
        mac = faker.word()

        with self.assertRaises(ValidationError):
            validate_mac(mac)
