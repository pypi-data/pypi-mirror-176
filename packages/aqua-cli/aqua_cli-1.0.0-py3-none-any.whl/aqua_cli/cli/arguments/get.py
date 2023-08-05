from aqua_cli.database import execute_query

def get(target):
    if target == 'get':
        day = execute_query.execute_query(
            query='SELECT day FROM aqua ORDER BY day DESC',
            return_value=True
        )
        
        intake = execute_query.execute_query(
            query='SELECT intake FROM aqua ORDER BY day DESC',
            return_value=True
        )

        print(f'Your intake [DAY {day[0]}]: {intake[0]}ml')
    elif target == 'get-all':
        info = execute_query.execute_query(
            query='SELECT * FROM aqua',
            return_value=True,
            return_all=True
        )

        print('Intake history:')
        for value in info:
            day = value[0]
            intake = value[1]
            goal = value[2]

            print(f' DAY {day}: {intake}/{goal}ml')