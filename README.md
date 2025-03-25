
### The Lovebugs
___

The group members are:

1. Ollie March
2. Lucas Shaw
3. Samuel Max Heslop
4. Hazel Goddard
5. Jan Van Wingerden
6. Dylan Hough
7. Alex Burnett


# Glapped

Galpped Is an all-new vintage and second-hand fashion trading for your Campus. Built with the django framework it can be easily hosted and run to enable students of your university to trade clothing, as well as driving engagement for environmental causes on campus.

## PROCESS DOCUMENTS
We use a trello/kanban board to manage our project, deligate tasks and track progress.

trello link: [https://trello.com/b/zUah14WH/glapped-board]

Snapshots of the trello/trello board as progress has been made can be found in the directory path below:

./process-documents/kanban-snapshots/

Group meeting notes can be found on trello/kanban, or additionally in the directory path below:

./process-documents/meeting-notes/


## TECHNICAL DOCUMENTS
Our techincal documentation can be found in our github below:

github link: [https://github.com/The-Lovebugs/Glapped]

We have also include the source code in the directory below:

./technical-documents/source-code/

## PRODUCT DOCUMENTS
All product documentation can be found as a pdf in the directory below:

./product-documents/documentation

Requirements analysis can be found at the following directory:

./product-documents/requirements-analysis

## PRESENTATION

The slides for the group presentation can be found in the following directory:

./presentation/

## POSTER

The poster for Glapped can be found in the following directory:

./poster/


## Installation

The project can be built and ran using Python, we recommend version 3.13.2 and up.
  
### Installing dependancies
With python installed to path - 
```bash
  pip install django pillow crispy-bootstrap4 daphne channels
```

  
Or, if using [Anaconda]("https://www.anaconda.com/download") - 

```bash
  conda create -n glapped_env python=3.13.2
```
then
```bash
  conda activate glapped_env
  pip install django pillow crispy-bootstrap4 daphne channels
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
![Register](https://i.imgur.com/ie5jv35.png)

You can register account on the site, via the join now button on the home page.

### Navigating listings
![Listings](https://i.imgur.com/Lg2xoIu.png)
Listings can be navigated via the homepage once logged in. To enter a listing, simply click on the the image and you'll be taken to its respective page.

### Creating a listing
![Listings](https://i.imgur.com/s63cncE.png)

In order to successfully create a listing, choose buy now or auction then complete the required fields and provide an html5 compatible image.

### View account information
![Listings](https://i.imgur.com/7l1sneZ.png)

In order to successfully create a listing, choose buy now or auction then complete the required fields and provide an html5 compatible image.

### View leaderboards
![Listings](https://i.imgur.com/tgrPsDx.png)

To view the public leaderboard of co2 and water saved by users, navigate to the leaderboard section in the navbar

### Glapchat
![Listings](https://i.imgur.com/WH7rPmB.png)

To view your current chats, navigate to glapchat in the navbar

## Administration
![Listings](https://i.imgur.com/w7rL5pP.png)
  
  

![Listings](https://i.imgur.com/iKc9gtx.png)
The Admin panel can be found at ```<hosted url>/admin/```   
  
In order to use an admin accuont, first create a super user via commandline. This can be done by performing the command -
  
```bash
  python manage.py createsuperuser
```

within the glapped folder, and then following the on-screen instructions.
