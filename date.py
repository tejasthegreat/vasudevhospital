from datetime import datetime
date='28042022'
date_object=datetime.strptime(date,'%d%m%Y')
date_format=datetime.strftime(date_object,'%d-%b-%y')


print(type(date_format))