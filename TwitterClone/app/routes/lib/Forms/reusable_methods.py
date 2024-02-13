from flask import flash, redirect, session

def print_form_debug_info(form):
    print('###################################')
    print()
    print('Form Data:')
    print(f'- Form: {form}')
    print(f'- Form Validation: {form.validate_on_submit()}')
    print()
    print('###################################')

def print_form_validation_failed(form):
    print('###################################')
    print()
    print(f'Form Validation Failed')
    print(f'- Form Errors: {form.errors}')
    print()
    print('###################################')

def print_form_csrf_token(form):
    print('###################################')
    print()
    print('Form Data:')
    print(f'- Form Token: {form.csrf_token.data}')
    print(f'- CSRF Session Token: {session.get("csrf_token")}')
    print(f'- Token equality: {form.csrf_token.data == session.get("_csrf_token")}')
    print()
    print('###################################')
