# Glapped

Glapped Is an all-new vintage and second-hand fashion trading for your Campus. Built with the django framework it can be easily hosted and run to enable students of your university to trade clothing, as well as driving engagement for environmental causes on campus.
## Demo

![Demo](https://i.imgur.com/7ZbCpY5.gif)
## Installation

The project can be built and ran using Python, we recommend version 3.13.2 and up.
  
### Installing dependencies
With python installed to path - 
```bash
  pip install django pillow crispy-bootstrap4
```

  
Or, if using [Anaconda]("https://www.anaconda.com/download") - 

```bash
  conda create -n glapped_env python=3.13.2
```
then
```bash
  conda activate glapped_env
  pip install django pillow crispy-bootstrap4
```
  
### Running the Server

First, download the current source code and locate the installed folder. Then Run - 
```bash
  cd <installed path>
  cd glapped
  python manage.py runserver
```

## Running Tests
In order to run unit tests, make sure you are in the installed project folder within a terminal, then run - 
```bash
  python manage.py test
```


## Usage/Examples
### Creating an account
![Register](https://i.imgur.com/fMlRktY.png)

You can register account on the site, either via the join now button on the home page, or by heading to ```<hosted url>/register/``` 

### Navigating listings
![Listings](https://i.imgur.com/c0DtoTy.png)
Listings can be navigated via the homepage once logged in. To enter a listing, simply click on the the image and you'll be taken to its respective page.

### Creating a listing
![Listings](https://i.imgur.com/Tfl01Ku.png)

In order to successfully create a listing, complete the required fields and provide an html5 compatible image.
## Administration
![Listings](https://i.imgur.com/w7rL5pP.png)
  
  

![Listings](https://i.imgur.com/iKc9gtx.png)
The Admin panel can be found at ```<hosted url>/admin/```   
  
In order to use an admin account, first create a super user via commandline. This can be done by performing the command -
  
```bash
  python manage.py createsuperuser
```

within the glapped folder, and then following the on-screen instructions.

## Authors

- [Hazel](https://github.com/coolduucks)
- [Alex](https://github.com/Cosmospacedog)
- [Dylan](https://github.com/Hayai1)
- [Jan](https://github.com/januaryvanwingerden)
- [Lucas](https://github.com/ls250)
- [Max](https://github.com/smh254)
- [Ollie](https://github.com/Ollie-March)
## License

[MIT](https://choosealicense.com/licenses/mit/)

