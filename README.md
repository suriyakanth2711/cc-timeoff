#  Time Off Appplication

Django application to manage time-off

![API Interaction](https://user-images.githubusercontent.com/62957689/228738983-202881ea-ffc2-4644-ae5b-2d4298dd74a7.png)

## API Referenc


|URL  | RESPONSE |
|--|--|
| GET /api/timeoff/policy/<organization\> | List of Policies in for a organization  |
| GET /api/timeoff/policy/<organization\>/<id\>  | Get Details of policy (with id) in a organization |
| POST /api/timeoff/policy/<organization\>/new  | Add a new policy in a organization |
| PATCH /api/timeoff/policy/<organization\>/<id\>  | Edit policy (with id) in a organization |
| DELETE /api/timeoff/policy/<organization\>/<id\>  | Delete policy (with id) in a organization |
| GET /api/timeoff/leaves/<organization\>/<eid\>  | Get leave Details of employee (with id) |
| POST /api/timeoff/leaves/<organization\>/<eid\> | Apply for a leave |



## Setup

 1. Clone the repository

	    git clone https://github.com/suriyakanth2711/cc-timeoff.git
	    cd cc-timeoff

 2. Setup a python >=3.8.5 environment

	    python -m venv .env

 3. Activate the virtual environment

	Windows
		
		.env\Scripts\activate

	Linux

		source .env/bin/activate

 4. Install required packages
	
	    pip install -r requirements.txt

 5. Make django migrations to setup the database
	 
		 python manage.py makemigrations
		 python manage.py migrate

 6. Run the server

	    python manage.py runserver 8080


The server should start on localhost:8080
