from flask import flash, redirect

def print_user_details(new_user):
    print('###################################')
    print()
    print(f'- id: {new_user.id}')
    print(f'- email: {new_user.email}')        
    print(f'- username: {new_user.username}')     
    print(f'- password: {new_user.password}')     
    print(f'- birth date: {new_user.birth_date}')  
    print() 
    print('###################################')

def print_user_serialization(user):
    print('###################################')
    print()
    print(f'- User: {user.serialize()}')
    print()
    print('###################################')
