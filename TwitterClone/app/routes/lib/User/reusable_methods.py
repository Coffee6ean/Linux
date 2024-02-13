from flask import flash, redirect

def print_user_details(user):
    print('###################################')
    print()
    print(f'- id: {user.id}')
    print(f'- email: {user.email}')        
    print(f'- username: {user.username}')     
    print(f'- password: {user.password}')     
    print(f'- birth date: {user.birth_date}')  
    print() 
    print('###################################')

def print_user_serialization(user):
    print('###################################')
    print()
    print(f'- User: {user.serialize()}')
    print()
    print('###################################')
