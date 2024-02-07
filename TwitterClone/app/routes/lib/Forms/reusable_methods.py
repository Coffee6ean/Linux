from flask import flash, redirect

def print_form_debug_info(form):
    print('###################################')
    print()
    print(f'- Form: {form}')
    print(f'- Form Validation: {form.validate_on_submit()}')
    print()
    print('###################################')

def print_form_validation_failed(form):
    print('###################################')
    print()
    print(f'- Form Validation Failed')
    print(f'- Form Errors: {form.errors}')
    print()
    print('###################################')
