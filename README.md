The source code (in \src) for this project is split into the following subdirectories: 

- database
- data_handling
- frames
- requests

The application is run via main.py in the \src directory. 
All interactions with the application are written in frames\search_menu.py
	- after searching or clicking the random option, an instance of PlayerResults or TeamResults is created
		- these classes exist in data_handling\player.py and data_handling\team.py
		- results are created by querying the database with queries defined in database\query
	- this is passed to frames\result_frame to display the results
	
Any new items that are displayed with results should be defined within the PlayerResults or TeamResults classes

as of 2/19/2025, the entire instance of PlayerResults or TeamResults is passed from validate_entry() in src\frames\search_menu to 
update_dashboard() (method of Dashboard class instance packed to ResultFrame instance, which is packed to the main window and updated
with each new search). 

also added team logo and player headshot pngs on 2/19/2025

* NOTE - i had to download msys2 ucrt64 to get the cairo package to work
	- this is what allows for proper searching and displaying of characters with accidentals