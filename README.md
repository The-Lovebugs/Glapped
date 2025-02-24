# Glapped

Galpped Is an all-new vintage and second-hand fashion trading for your Campus. Built with the django framework it can be easily hosted and run to enable students of your university to trade clothing, as well as driving engagement for environmental causes on campus.
## Demo

![Demo](https://i.imgur.com/QgItKDi.gif)
## Installation

The project can be built and ran using Python, we recommend version 3.13.2 and up.
  
### Installing dependancies
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

## Usage/Examples

### Creating an account
You can register account on the site, either via the join now button on the home page, or by heading to ```<hosted url>/register/``` 

### Navigating listings
Listings can be navigated via the homepage once logged in. To enter a listing, simply click on the the image and you'll be taken to its respective page.


## Administration
The Admin panel can be found at ```<hosted url>/admin/```   
  
In order to use an admin accuont, first create a super user via commandline. This can be done by performing the command -
  
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

