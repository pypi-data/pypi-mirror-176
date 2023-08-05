from aqua_cli.database import execute_query

def change_amount(target, amount):
    day = execute_query.execute_query(
        query='SELECT day FROM aqua ORDER BY day DESC',
        return_value=True
    )
    
    current_intake = execute_query.execute_query(
        query='SELECT intake FROM aqua ORDER BY day DESC',
        return_value=True
    )

    intake = current_intake[0]
    new_intake = 0

    if amount <= 0:
        print('ERROR: invalid amount.')
        return
    
    if target == 'add':
        new_intake = intake + amount
        print(f'Added {amount}ml.')
    elif target == 'remove':
        new_intake = intake - amount
        
        if intake <= 0:
            print('Your intake is currently 0, you can\'t remove.')
            return
        if new_intake <= 0:
            print('If you remove this amount, your intake will be less than zero.')
            return

        print(f'Removed {amount}ml.')

    execute_query.execute_query(
        query='UPDATE aqua SET intake = ? WHERE day = ?',
        parameters=[new_intake, day[0]]
    )