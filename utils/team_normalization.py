# utils/team_normalization.py

from __future__ import annotations
from difflib import SequenceMatcher
import string

__all__ = ["normalize_team_name"]

# -----------------------------------------------------------------------------
# TEAM_MAP_OVERRIDES
# -----------------------------------------------------------------------------
# These are hard overrides for known problem cases where:
# - Source sites use ambiguous or conflicting names
# - Multiple schools share similar labels
# - You want to force a specific canonical TR name regardless of fuzzy logic
#
# Keys = raw incoming names
# Values = final canonical TR name (exactly as used in your TR tables)
TEAM_MAP_OVERRIDES = {
    # Saint / St conflicts
    "Saint Joseph's": "St Josephs",
    "Saint Josephs": "St Josephs",
    "Saint Josephs (PA)": "St Josephs",
    "Saint Louis": "St Louis",
    "Saint Mary's": "St Marys",
    "Saint Marys": "St Marys",
    "Saint Mary's (CA)": "St Marys",
    "Saint Peter's": "St Peters",
    "Saint Peters": "St Peters",

    # Directional / multi-campus clarifications
    "Miami (FL)": "Miami FL",
    "Miami Florida": "Miami FL",
    "Miami (OH)": "Miami OH",
    "Miami Ohio": "Miami OH",
    "Central Florida": "UCF",
    "UCF Knights": "UCF",
    "South Florida": "USF",
    "USF Bulls": "USF",

    # UNC family
    "North Carolina Tar Heels": "North Carolina",
    "UNC Tar Heels": "North Carolina",
    "UNC": "North Carolina",
    "UNC-Chapel Hill": "North Carolina",

    # Texas A&M variants
    "Texas A&M–Corpus Christi": "Texas A&M-CC",
    "Texas A&M Corpus Christi": "Texas A&M-CC",
    "Texas A&M CC": "Texas A&M-CC",
    "Texas A&M-Corpus Christi Islanders": "Texas A&M-CC",

    # Misc high‑profile clarifications
    "UConn": "Connecticut",
    "UConn Huskies": "Connecticut",
    "LSU Tigers": "LSU",
    "Ole Miss Rebels": "Ole Miss",
    "Mississippi Rebels": "Ole Miss",
    "Southern Cal": "USC",
    "USC Trojans": "USC",
    "Arizona St": "Arizona State",
    "Arizona St.": "Arizona State",
    "Florida St": "Florida State",
    "Florida St.": "Florida State",
}

# -----------------------------------------------------------------------------
# NORMALIZE (flat, alias → canonical TR name)
# -----------------------------------------------------------------------------
# Keys  = every alias / spelling / punctuation / spacing / mascot variant
# Values = single canonical TR team name (Team_TR)
#
# NOTE: This is a representative subset. Extend freely by following the pattern.
NORMALIZE= {
   "Abilene Christian": "Abl Christian", "Abilene Chr": "Abl Christian", "Abilene Christian Univ": "Abl Christian", "Abilene Christian Wildcats": "Abl Christian",
"Air Force": "Air Force", "Air Force Falcons": "Air Force", "Air Force Academy": "Air Force","Akron": "Akron", "Akron Zips": "Akron",
"Alabama": "Alabama", "Alabama Crimson Tide": "Alabama",
"Alabama A&M": "Alabama A&M", "Alabama A and M": "Alabama A&M", "Alabama A&M Bulldogs": "Alabama A&M","Alabama St": "Alabama St", "Alabama St.": "Alabama St", "Alabama State": "Alabama St", "Alabama State Hornets": "Alabama St",
"Albany": "Albany", "Albany Great Danes": "Albany", "UAlbany": "Albany",
"Alcorn St": "Alcorn St", "Alcorn State": "Alcorn St", "Alcorn St.": "Alcorn St", "Alcorn State Braves": "Alcorn St",
"American": "American", "American Univ": "American", "American University": "American", "American Eagles": "American",
"App State": "App State", "Appalachian State": "App State", "Appalachian St": "App State", "Appalachian St.": "App State", "App State Mountaineers": "App State",
"Arizona": "Arizona", "Arizona Wildcats": "Arizona",
"Arizona St": "Arizona St", "Arizona St.": "Arizona St", "Arizona State": "Arizona St", "Arizona State Sun Devils": "Arizona St",
"Arkansas": "Arkansas", "Arkansas Razorbacks": "Arkansas",
"Arkansas St": "Arkansas St", "Arkansas St.": "Arkansas St", "Arkansas State": "Arkansas St", "Arkansas State Red Wolves": "Arkansas St",
"Army": "Army", "Army West Point": "Army", "Army Black Knights": "Army",
"AR-Pine Bluff": "AR-Pine Bluff", "Arkansas Pine Bluff": "AR-Pine Bluff", "Ark-Pine Bluff": "AR-Pine Bluff", "Ark Pine Bluff": "AR-Pine Bluff", "UAPB": "AR-Pine Bluff",
"Auburn": "Auburn", "Auburn Tigers": "Auburn",
"Austin Peay": "Austin Peay", "Austin Peay St": "Austin Peay", "Austin Peay State": "Austin Peay", "Austin Peay Governors": "Austin Peay",
"Ball St": "Ball St", "Ball St.": "Ball St", "Ball State": "Ball St", "Ball State Cardinals": "Ball St","Baylor": "Baylor", "Baylor Bears": "Baylor",
"Bellarmine": "Bellarmine", "Bellarmine Knights": "Bellarmine",
"Belmont": "Belmont", "Belmont Bruins": "Belmont",
"Bethune": "Bethune", "Bethune Cookman": "Bethune", "Bethune-Cookman": "Bethune", "Bethune Cookman Wildcats": "Bethune",
"Binghamton": "Binghamton", "Binghamton Bearcats": "Binghamton",
"Boise St": "Boise St", "Boise St.": "Boise St", "Boise State": "Boise St", "Boise State Broncos": "Boise St",
"Boston College": "Boston College", "BC": "Boston College", "Boston College Eagles": "Boston College","Boston U": "Boston U", "Boston Univ": "Boston U", "Boston University": "Boston U", "Boston University Terriers": "Boston U",
"Bowling Green": "Bowling Green", "Bowling Green St": "Bowling Green", "Bowling Green State": "Bowling Green", "Bowling Green Falcons": "Bowling Green",
"Bradley": "Bradley", "Bradley Braves": "Bradley",
"Brown": "Brown", "Brown Bears": "Brown",
"Bryant": "Bryant", "Bryant Bulldogs": "Bryant",
"Bucknell": "Bucknell", "Bucknell Bison": "Bucknell",
"Buffalo": "Buffalo", "Buffalo Bulls": "Buffalo", "UB": "Buffalo",
"Butler": "Butler", "Butler Bulldogs": "Butler",
"BYU": "BYU", "Brigham Young": "BYU", "Brigham Young Cougars": "BYU",
"C Arkansas": "C Arkansas", "Central Arkansas": "C Arkansas", "Central Ark": "C Arkansas", "Central Ark.": "C Arkansas", "Central Arkansas Bears": "C Arkansas",
"C Connecticut": "C Connecticut", "Central Connecticut": "C Connecticut", "Central Conn": "C Connecticut", "Central Conn.": "C Connecticut", "Central Connecticut St": "C Connecticut", "Central Connecticut State": "C Connecticut", "CCSU": "C Connecticut",
"C Michigan": "C Michigan", "Central Michigan": "C Michigan", "Central Mich": "C Michigan", "Central Mich.": "C Michigan", "Central Michigan Chippewas": "C Michigan",
"Cal Baptist": "Cal Baptist", "California Baptist": "Cal Baptist", "Cal Bap": "Cal Baptist", "Cal Bap.": "Cal Baptist", "California Baptist Lancers": "Cal Baptist",
"Cal Poly": "Cal Poly", "Cal Poly SLO": "Cal Poly", "Cal Poly Mustangs": "Cal Poly",
"California": "California", "Cal": "California", "California Golden Bears": "California","Campbell": "Campbell", "Campbell Fighting Camels": "Campbell",
"Canisius": "Canisius", "Canisius Golden Griffins": "Canisius",
"Charleston": "Charleston", "College of Charleston": "Charleston", "Charleston Cougars": "Charleston","Charleston So": "Charleston So", "Charleston Southern": "Charleston So", "Charleston Southern Buccaneers": "Charleston So",
"Charlotte": "Charlotte", "Charlotte 49ers": "Charlotte",
"Chattanooga": "Chattanooga", "Chattanooga Mocs": "Chattanooga",
"Chicago St": "Chicago St", "Chicago State": "Chicago St", "Chicago St.": "Chicago St", "Chicago State Cougars": "Chicago St",
"Cincinnati": "Cincinnati", "Cincinnati Bearcats": "Cincinnati",
"Clemson": "Clemson", "Clemson Tigers": "Clemson",
"Cleveland St": "Cleveland St", "Cleveland St.": "Cleveland St", "Cleveland State": "Cleveland St", "Cleveland State Vikings": "Cleveland St",
"Coastal Car": "Coastal Car", "Coastal Carolina": "Coastal Car", "Coastal Carolina Chanticleers": "Coastal Car",
"Colgate": "Colgate", "Colgate Raiders": "Colgate",
"Colorado": "Colorado", "Colorado Buffaloes": "Colorado",
"Colorado St": "Colorado St", "Colorado St.": "Colorado St", "Colorado State": "Colorado St", "Colorado State Rams": "Colorado St",
"Columbia": "Columbia", "Columbia Lions": "Columbia",
"Coppin St": "Coppin St", "Coppin St.": "Coppin St", "Coppin State": "Coppin St", "Coppin State Eagles": "Coppin St",
"Cornell": "Cornell", "Cornell Big Red": "Cornell",
"Creighton": "Creighton", "Creighton Bluejays": "Creighton",
"CS Bakersfield": "CS Bakersfield", "Cal St Bakersfield": "CS Bakersfield", "Cal State Bakersfield": "CS Bakersfield", "CSU Bakersfield": "CS Bakersfield", "Cal State Bakersfield Roadrunners": "CS Bakersfield",
"CS Fullerton": "CS Fullerton", "Cal St Fullerton": "CS Fullerton", "Cal State Fullerton": "CS Fullerton", "CSU Fullerton": "CS Fullerton", "Cal State Fullerton Titans": "CS Fullerton","CS Northridge": "CS Northridge", "Cal St Northridge": "CS Northridge", "Cal State Northridge": "CS Northridge", "CSU Northridge": "CS Northridge", "Cal State Northridge Matadors": "CS Northridge", "CSU": "CSU",  # passthrough for ambiguous “CSU” inputs when no specific campus is implied
"Dartmouth": "Dartmouth", "Dartmouth Big Green": "Dartmouth",
"Davidson": "Davidson", "Davidson Wildcats": "Davidson",
"Dayton": "Dayton", "Dayton Flyers": "Dayton",
"Delaware": "Delaware", "Delaware Blue Hens": "Delaware",
"Delaware St": "Delaware St", "Delaware St.": "Delaware St", "Delaware State": "Delaware St", "Delaware State Hornets": "Delaware St",
"Denver": "Denver", "Denver Pioneers": "Denver",
"DePaul": "DePaul", "DePaul Blue Demons": "DePaul",
"Detroit Mercy": "Detroit Mercy", "Detroit": "Detroit Mercy", "Detroit Titans": "Detroit Mercy", "Detroit Mercy Titans": "Detroit Mercy",
"Drake": "Drake", "Drake Bulldogs": "Drake",
"Drexel": "Drexel", "Drexel Dragons": "Drexel",
"Duke": "Duke", "Duke Blue Devils": "Duke",
"Duquesne": "Duquesne", "Duquesne Dukes": "Duquesne",
"E Carolina": "E Carolina", "East Carolina": "E Carolina", "ECU": "E Carolina", "East Carolina Pirates": "E Carolina",
"E Illinois": "E Illinois", "E Illinois.": "E Illinois", "East Illinois": "E Illinois", "Eastern Illinois": "E Illinois", "Eastern Illinois Panthers": "E Illinois","E Kentucky": "E Kentucky", "East Kentucky": "E Kentucky", "Eastern Kentucky": "E Kentucky", "Eastern Kentucky Colonels": "E Kentucky",
"E Michigan": "E Michigan", "East Michigan": "E Michigan", "Eastern Michigan": "E Michigan", "Eastern Michigan Eagles": "E Michigan",
"E Tennessee St": "E Tennessee St", "ETSU": "E Tennessee St", "East Tennessee St": "E Tennessee St", "East Tennessee State": "E Tennessee St", "E Tennessee St.": "E Tennessee St", "Eastern Tennessee State": "E Tennessee St", "East Tennessee State Buccaneers": "E Tennessee St",
"E Texas A&M": "E Texas A&M", "East Texas A&M": "E Texas A&M", "Texas A&M Commerce": "E Texas A&M", "Texas A&M–Commerce": "E Texas A&M", "Texas A&M Commerce Lions": "E Texas A&M","E Washington": "E Washington", "East Washington": "E Washington", "Eastern Washington": "E Washington", "Eastern Washington Eagles": "E Washington",
"Elon": "Elon", "Elon Phoenix": "Elon",
"Evansville": "Evansville", "Evansville Aces": "Evansville",
"F Dickinson": "F Dickinson", "Fairleigh Dickinson": "F Dickinson", "Fairleigh Dickinson Knights": "F Dickinson",
"Fairfield": "Fairfield", "Fairfield Stags": "Fairfield",
"FGCU": "FGCU", "Florida Gulf Coast": "FGCU", "Florida Gulf Coast Eagles": "FGCU",
"Florida": "Florida", "Florida Gators": "Florida",
"Florida A&M": "Florida A&M", "Florida A and M": "Florida A&M", "Florida A&M Rattlers": "Florida A&M",
"Florida Atlantic": "Florida Atlantic", "FAU": "Florida Atlantic", "Florida Atlantic Owls": "Florida Atlantic",
"Florida Intl": "Florida Intl", "Florida International": "Florida Intl", "FIU": "Florida Intl", "Florida International Panthers": "Florida Intl",
"Florida St": "Florida St", "Florida St.": "Florida St", "Florida State": "Florida St", "Florida State Seminoles": "Florida St",
"Fordham": "Fordham", "Fordham Rams": "Fordham",
"Fresno St": "Fresno St", "Fresno St.": "Fresno St", "Fresno State": "Fresno St", "Fresno State Bulldogs": "Fresno St",
"Furman": "Furman", "Furman Paladins": "Furman",
"G Washington": "G Washington", "George Washington": "G Washington", "George Washington Colonials": "G Washington", "GW": "G Washington",
"Gardner-Webb": "Gardner-Webb", "Gardner Webb": "Gardner-Webb", "Gardner-Webb Runnin' Bulldogs": "Gardner-Webb","George Mason": "George Mason", "GMU": "George Mason", "George Mason Patriots": "George Mason","Georgetown": "Georgetown", "Georgetown Hoyas": "Georgetown","Georgia": "Georgia", "Georgia Bulldogs": "Georgia",
"Georgia So": "Georgia So", "Georgia Southern": "Georgia So", "Georgia Southern Eagles": "Georgia So","Georgia St": "Georgia St", "Georgia St.": "Georgia St", "Georgia State": "Georgia St", "Georgia State Panthers": "Georgia St",
"Georgia Tech": "Georgia Tech", "Georgia Institute of Technology": "Georgia Tech", "Georgia Tech Yellow Jackets": "Georgia Tech",
"Gonzaga": "Gonzaga", "Gonzaga Bulldogs": "Gonzaga",
"Grambling": "Grambling", "Grambling St": "Grambling", "Grambling State": "Grambling", "Grambling State Tigers": "Grambling",
"Grand Canyon": "Grand Canyon", "GCU": "Grand Canyon", "Grand Canyon Lopes": "Grand Canyon","Green Bay": "Green Bay", "UW Green Bay": "Green Bay", "Green Bay Phoenix": "Green Bay","Hampton": "Hampton", "Hampton Pirates": "Hampton",
"Hampton": "Hampton", "Hampton Pirates": "Hampton",
"Harvard": "Harvard", "Harvard Crimson": "Harvard",
"Hawai'i": "Hawai'i", "Hawaii": "Hawai'i", "Univ of Hawaii": "Hawai'i", "Hawaii Rainbow Warriors": "Hawai'i",
"High Point": "High Point", "High Point Panthers": "High Point",
"Hofstra": "Hofstra", "Hofstra Pride": "Hofstra",
"Holy Cross": "Holy Cross", "Holy Cross Crusaders": "Holy Cross",
"Hou Christian": "Hou Christian", "Houston Christian": "Hou Christian", "HCU": "Hou Christian", "Houston Christian Huskies": "Hou Christian",
"Houston": "Houston", "Houston Cougars": "Houston",
"Howard": "Howard", "Howard Bison": "Howard",
"Idaho": "Idaho", "Idaho Vandals": "Idaho",
"Idaho St": "Idaho St", "Idaho St.": "Idaho St", "Idaho State": "Idaho St", "Idaho State Bengals": "Idaho St","Illinois": "Illinois", "Illinois Fighting Illini": "Illinois","Illinois Chicago": "Illinois Chicago", "UIC": "Illinois Chicago", "Illinois-Chicago": "Illinois Chicago", "Illinois Chicago Flames": "Illinois Chicago",
"Illinois St": "Illinois St", "Illinois St.": "Illinois St", "Illinois State": "Illinois St", "Illinois State Redbirds": "Illinois St",
"Incarnate Word": "Incarnate Word", "UIW": "Incarnate Word", "Incarnate Word Cardinals": "Incarnate Word",
"Indiana": "Indiana", "Indiana Hoosiers": "Indiana",
"Indiana St": "Indiana St", "Indiana St.": "Indiana St", "Indiana State": "Indiana St", "Indiana State Sycamores": "Indiana St",
"Iona": "Iona", "Iona Gaels": "Iona",
"Iowa": "Iowa", "Iowa Hawkeyes": "Iowa",
"Iowa St": "Iowa St", "Iowa St.": "Iowa St", "Iowa State": "Iowa St", "Iowa State Cyclones": "Iowa St",
"IU Indy": "IU Indy", "Indiana Univ Indianapolis": "IU Indy", "IUPUI": "IU Indy",  # legacy alias "IU Indy Jaguars": "IU Indy",
"J Madison": "J Madison", "James Madison": "J Madison", "James Madison Dukes": "J Madison","Jackson St": "Jackson St", "Jackson St.": "Jackson St", "Jackson State": "Jackson St", "Jackson State Tigers": "Jackson St",
"Jacksonville": "Jacksonville", "Jacksonville Dolphins": "Jacksonville",
"Jacksonville St": "Jacksonville St", "Jacksonville St.": "Jacksonville St", "Jacksonville State": "Jacksonville St", "Jacksonville State Gamecocks": "Jacksonville St","Kansas": "Kansas", "Kansas Jayhawks": "Kansas",
"Kansas City": "Kansas City", "UMKC": "Kansas City", "Kansas City Roos": "Kansas City","Kansas St": "Kansas St", "Kansas St.": "Kansas St", "Kansas State": "Kansas St", "Kansas State Wildcats": "Kansas St",
"Kennesaw St": "Kennesaw St", "Kennesaw St.": "Kennesaw St", "Kennesaw State": "Kennesaw St", "Kennesaw State Owls": "Kennesaw St",
"Kent St": "Kent St", "Kent St.": "Kent St", "Kent State": "Kent St", "Kent State Golden Flashes": "Kent St",
"Kentucky": "Kentucky", "Kentucky Wildcats": "Kentucky",
"La Salle": "La Salle", "LaSalle": "La Salle", "La Salle Explorers": "La Salle",
"Lafayette": "Lafayette", "Lafayette Leopards": "Lafayette",
"Lamar": "Lamar", "Lamar Cardinals": "Lamar",
"Le Moyne": "Le Moyne", "LeMoyne": "Le Moyne", "Le Moyne Dolphins": "Le Moyne",
"Lehigh": "Lehigh", "Lehigh Mountain Hawks": "Lehigh",
"Liberty": "Liberty", "Liberty Flames": "Liberty",
"Lindenwood": "Lindenwood", "Lindenwood Lions": "Lindenwood",
"Lipscomb": "Lipscomb", "Lipscomb Bisons": "Lipscomb",
"Little Rock": "Little Rock", "Arkansas Little Rock": "Little Rock", "UALR": "Little Rock", "Little Rock Trojans": "Little Rock",
"LIU": "LIU", "Long Island": "LIU", "Long Island Univ": "LIU", "LIU Sharks": "LIU",
"Long Beach St": "Long Beach St", "Long Beach St.": "Long Beach St", "Long Beach State": "Long Beach St", "LBSU": "Long Beach St", "Long Beach State Beach": "Long Beach St","Longwood": "Longwood", "Longwood Lancers": "Longwood",
"Louisiana": "Louisiana", "Louisiana Lafayette": "Louisiana", "ULL": "Louisiana", "Louisiana Ragin' Cajuns": "Louisiana",
"Louisiana Tech": "Louisiana Tech", "La Tech": "Louisiana Tech", "Louisiana Tech Bulldogs": "Louisiana Tech",
"Louisville": "Louisville", "Louisville Cardinals": "Louisville",
"Loyola Chi": "Loyola Chi", "Loyola Chicago": "Loyola Chi", "Loyola-Chicago": "Loyola Chi", "Loyola Chicago Ramblers": "Loyola Chi",
"Loyola MD": "Loyola MD", "Loyola Maryland": "Loyola MD", "Loyola (MD)": "Loyola MD", "Loyola Maryland Greyhounds": "Loyola MD",
"Loyola Mymt": "Loyola Mymt", "Loyola Marymount": "Loyola Mymt", "LMU": "Loyola Mymt", "Loyola Marymount Lions": "Loyola Mymt",
"LSU": "LSU", "Louisiana State": "LSU", "LSU Tigers": "LSU",
"Maine": "Maine", "Maine Black Bears": "Maine",
"Manhattan": "Manhattan", "Manhattan Jaspers": "Manhattan",
"Marist": "Marist", "Marist Red Foxes": "Marist",
"Marquette": "Marquette", "Marquette Golden Eagles": "Marquette",
"Marshall": "Marshall", "Marshall Thundering Herd": "Marshall",
"Maryland": "Maryland", "Maryland Terrapins": "Maryland",
"Maryland ES": "Maryland ES", "Maryland Eastern Shore": "Maryland ES", "UMES": "Maryland ES", "Maryland Eastern Shore Hawks": "Maryland ES",
"McNeese": "McNeese", "McNeese St": "McNeese", "McNeese State": "McNeese", "McNeese Cowboys": "McNeese",
"Memphis": "Memphis", "Memphis Tigers": "Memphis",
"Mercer": "Mercer", "Mercer Bears": "Mercer",
"Mercyhurst": "Mercyhurst", "Mercyhurst Lakers": "Mercyhurst",
"Merrimack": "Merrimack", "Merrimack Warriors": "Merrimack",
"Miami": "Miami", "Miami FL": "Miami", "Miami Hurricanes": "Miami", "Miami (FL)": "Miami",
"Miami OH": "Miami OH", "Miami (OH)": "Miami OH", "Miami Ohio": "Miami OH", "Miami OH RedHawks": "Miami OH",
"Michigan": "Michigan", "Michigan Wolverines": "Michigan",
"Michigan St": "Michigan St", "Michigan St.": "Michigan St", "Michigan State": "Michigan St", "Michigan State Spartans": "Michigan St","Middle Tenn": "Middle Tenn", "Middle Tennessee": "Middle Tenn", "Middle Tennessee St": "Middle Tenn", "Middle Tennessee State": "Middle Tenn", "Middle Tennessee Blue Raiders": "Middle Tenn",
"Milwaukee": "Milwaukee", "UW Milwaukee": "Milwaukee", "Milwaukee Panthers": "Milwaukee",
"Minnesota": "Minnesota", "Minnesota Golden Gophers": "Minnesota",
"Miss Valley St": "Miss Valley St", "Mississippi Valley St": "Miss Valley St", "Mississippi Valley State": "Miss Valley St","Mississippi": "Mississippi", "Ole Miss": "Mississippi", "Mississippi Rebels": "Mississippi",
"Mississippi St": "Mississippi St", "Mississippi St.": "Mississippi St", "Mississippi State": "Mississippi St", "Miss St": "Mississippi St", "Mississippi State Bulldogs": "Mississippi St",
"Missouri": "Missouri", "Mizzou": "Missouri", "Missouri Tigers": "Missouri",
"Missouri St": "Missouri St", "Missouri St.": "Missouri St", "Missouri State": "Missouri St", "Missouri State Bears": "Missouri St",
"Monmouth": "Monmouth", "Monmouth Hawks": "Monmouth",
"Montana": "Montana", "Montana Grizzlies": "Montana",
"Montana St": "Montana St", "Montana St.": "Montana St", "Montana State": "Montana St", "Montana State Bobcats": "Montana St",
"Morehead St": "Morehead St", "Morehead St.": "Morehead St", "Morehead State": "Morehead St", "Morehead State Eagles": "Morehead St",
"Morgan St": "Morgan St", "Morgan St.": "Morgan St", "Morgan State": "Morgan St", "Morgan State Bears": "Morgan St",
"Mt St Mary's": "Mt St Mary's", "Mount St Mary's": "Mt St Mary's", "Mount St. Mary's": "Mt St Mary's", "MSM": "Mt St Mary's", "Mount St Marys": "Mt St Mary's", "Mountaineers (MSM)": "Mt St Mary's",
"Murray St": "Murray St", "Murray St.": "Murray St", "Murray State": "Murray St", "Murray State Racers": "Murray St",
"N Alabama": "N Alabama", "North Alabama": "N Alabama", "North Alabama Lions": "N Alabama",
"N Arizona": "N Arizona", "NAU": "N Arizona", "North Arizona": "N Arizona", "Northern Arizona": "N Arizona", "Northern Arizona Lumberjacks": "N Arizona",
"N Colorado": "N Colorado", "North Colorado": "N Colorado", "Northern Colorado": "N Colorado", "Northern Colorado Bears": "N Colorado",
"N Dakota St": "N Dakota St", "North Dakota St": "N Dakota St", "North Dakota State": "N Dakota St", "NDSU": "N Dakota St", "North Dakota State Bison": "N Dakota St",
"N Florida": "N Florida", "North Florida": "N Florida", "UNF": "N Florida", "North Florida Ospreys": "N Florida",
"N Illinois": "N Illinois", "North Illinois": "N Illinois", "Northern Illinois": "N Illinois", "NIU": "N Illinois", "Northern Illinois Huskies": "N Illinois",
"N Iowa": "N Iowa", "North Iowa": "N Iowa", "Northern Iowa": "N Iowa", "UNI": "N Iowa", "Northern Iowa Panthers": "N Iowa",
"N Kentucky": "N Kentucky", "North Kentucky": "N Kentucky", "Northern Kentucky": "N Kentucky", "NKU": "N Kentucky", "Northern Kentucky Norse": "N Kentucky",
"N Texas": "N Texas", "North Texas": "N Texas", "UNT": "N Texas", "North Texas Mean Green": "N Texas",
"Navy": "Navy", "Naval Academy": "Navy", "Navy Midshipmen": "Navy",
"NC A&T": "NC A&T", "North Carolina A&T": "NC A&T", "NC A and T": "NC A&T", "North Carolina A&T Aggies": "NC A&T",
"NC Asheville": "NC Asheville", "UNC Asheville": "NC Asheville", "North Carolina Asheville": "NC Asheville", "UNC Asheville Bulldogs": "NC Asheville",
"NC Central": "NC Central", "North Carolina Central": "NC Central", "NCCU": "NC Central", "North Carolina Central Eagles": "NC Central",
"NC Greensboro": "NC Greensboro", "UNC Greensboro": "NC Greensboro", "UNCG": "NC Greensboro", "North Carolina Greensboro": "NC Greensboro", "UNC Greensboro Spartans": "NC Greensboro",
"NC State": "NC State", "North Carolina State": "NC State", "NCSU": "NC State", "NC State Wolfpack": "NC State",
"NC Wilmington": "NC Wilmington", "UNC Wilmington": "NC Wilmington", "UNCW": "NC Wilmington", "North Carolina Wilmington": "NC Wilmington", "UNC Wilmington Seahawks": "NC Wilmington",
"Nebraska": "Nebraska", "Nebraska Cornhuskers": "Nebraska",
"Nevada": "Nevada", "Nevada Wolf Pack": "Nevada",
"New Hampshire": "New Hampshire", "UNH": "New Hampshire", "New Hampshire Wildcats": "New Hampshire",
"New Mexico": "New Mexico", "UNM": "New Mexico", "New Mexico Lobos": "New Mexico",
"New Mexico St": "New Mexico St", "New Mexico St.": "New Mexico St", "New Mexico State": "New Mexico St", "NMSU": "New Mexico St", "New Mexico State Aggies": "New Mexico St",
"New Orleans": "New Orleans", "UNO": "New Orleans", "New Orleans Privateers": "New Orleans",
"Niagara": "Niagara", "Niagara Purple Eagles": "Niagara",
"Nicholls": "Nicholls", "Nicholls St": "Nicholls", "Nicholls State": "Nicholls", "Nicholls Colonels": "Nicholls",
"NJIT": "NJIT", "New Jersey Institute of Technology": "NJIT", "NJIT Highlanders": "NJIT",
"Norfolk St": "Norfolk St", "Norfolk St.": "Norfolk St", "Norfolk State": "Norfolk St", "Norfolk State Spartans": "Norfolk St",
"North Carolina": "North Carolina", "UNC": "North Carolina", "North Carolina Tar Heels": "North Carolina",
"North Dakota": "North Dakota", "UND": "North Dakota", "North Dakota Fighting Hawks": "North Dakota",
"Northeastern": "Northeastern", "Northeastern Huskies": "Northeastern",
"Northwestern": "Northwestern", "Northwestern Wildcats": "Northwestern",
"Notre Dame": "Notre Dame", "Notre Dame Fighting Irish": "Notre Dame",
"NW State": "NW State", "Northwestern State": "NW State", "Northwestern St": "NW State", "Northwestern State Demons": "NW State","Oakland": "Oakland", "Oakland Golden Grizzlies": "Oakland","Ohio":"Ohio","Ohio Bobcats":"Ohio",
"Ohio St": "Ohio St", "Ohio St.": "Ohio St", "Ohio State": "Ohio St", "Ohio State Buckeyes": "Ohio St",
"Oklahoma": "Oklahoma", "Oklahoma Sooners": "Oklahoma",
"Oklahoma St": "Oklahoma St", "Oklahoma St.": "Oklahoma St", "Oklahoma State": "Oklahoma St", "Oklahoma State Cowboys": "Oklahoma St",
"Old Dominion": "Old Dominion", "ODU": "Old Dominion", "Old Dominion Monarchs": "Old Dominion",
"Omaha": "Omaha", "Nebraska Omaha": "Omaha", "UNO Mavericks": "Omaha",
"Oral Roberts": "Oral Roberts", "ORU": "Oral Roberts", "Oral Roberts Golden Eagles": "Oral Roberts",
"Oregon": "Oregon", "Oregon Ducks": "Oregon",
"Oregon St": "Oregon St", "Oregon St.": "Oregon St", "Oregon State": "Oregon St", "Oregon State Beavers": "Oregon St",
"Pacific": "Pacific", "Pacific Tigers": "Pacific",
"Penn": "Penn", "Pennsylvania": "Penn", "UPenn": "Penn", "Penn Quakers": "Penn",
"Penn St": "Penn St", "Penn St.": "Penn St", "Penn State": "Penn St", "Penn State Nittany Lions": "Penn St",
"Pepperdine": "Pepperdine", "Pepperdine Waves": "Pepperdine",
"Pittsburgh": "Pittsburgh", "Pitt": "Pittsburgh", "Pittsburgh Panthers": "Pittsburgh",
"Portland": "Portland", "Portland Pilots": "Portland",
"Portland St": "Portland St", "Portland St.": "Portland St", "Portland State": "Portland St", "Portland State Vikings": "Portland St",
"Prairie View": "Prairie View", "Prairie View A&M": "Prairie View", "PVAMU": "Prairie View", "Prairie View A&M Panthers": "Prairie View",
"Presbyterian": "Presbyterian", "Presbyterian Blue Hose": "Presbyterian",
"Princeton": "Princeton", "Princeton Tigers": "Princeton",
"Providence": "Providence", "Providence Friars": "Providence",
"Purdue": "Purdue", "Purdue Boilermakers": "Purdue",
"Purdue FW": "Purdue FW", "Purdue Fort Wayne": "Purdue FW", "PFW": "Purdue FW", "Purdue Fort Wayne Mastodons": "Purdue FW",
"Queens": "Queens", "Queens Univ": "Queens", "Queens Royals": "Queens",
"Quinnipiac": "Quinnipiac", "Quinnipiac Bobcats": "Quinnipiac",
"Radford": "Radford", "Radford Highlanders": "Radford",
"Rhode Island": "Rhode Island", "URI": "Rhode Island", "Rhode Island Rams": "Rhode Island",
"Rice": "Rice", "Rice Owls": "Rice",
"Richmond": "Richmond", "Richmond Spiders": "Richmond",
"Rider": "Rider", "Rider Broncs": "Rider",
"Robert Morris": "Robert Morris", "RMU": "Robert Morris", "Robert Morris Colonials": "Robert Morris",
"Rutgers": "Rutgers", "Rutgers Scarlet Knights": "Rutgers",
"S Alabama": "S Alabama", "South Alabama": "S Alabama", "South Alabama Jaguars": "S Alabama",
"S Carolina St": "S Carolina St", "South Carolina St": "S Carolina St", "South Carolina State": "S Carolina St", "South Carolina State Bulldogs": "S Carolina St",
"S Dakota St": "S Dakota St", "South Dakota St": "S Dakota St", "South Dakota State": "S Dakota St", "SDSU (SD State)": "S Dakota St", "South Dakota State Jackrabbits": "S Dakota St",
"S Florida": "S Florida", "South Florida": "S Florida", "USF": "S Florida", "South Florida Bulls": "S Florida",
"S Illinois": "S Illinois", "Southern Illinois": "S Illinois", "SIU": "S Illinois", "Southern Illinois Salukis": "S Illinois",
"S Indiana": "S Indiana", "Southern Indiana": "S Indiana", "Southern Indiana Screaming Eagles": "S Indiana",
"S Utah": "S Utah", "Southern Utah": "S Utah", "Southern Utah Thunderbirds": "S Utah",
"Sacramento St": "Sacramento St", "Sacramento St.": "Sacramento St", "Sacramento State": "Sacramento St", "Sac State": "Sacramento St", "Sacramento State Hornets": "Sacramento St",
"Sacred Heart": "Sacred Heart", "Sacred Heart Pioneers": "Sacred Heart",
"Saint Joseph's": "Saint Joseph's", "St Josephs": "Saint Joseph's", "St Joseph's": "Saint Joseph's", "Saint Josephs": "Saint Joseph's", "Saint Joseph's Hawks": "Saint Joseph's",
"Saint Louis": "Saint Louis", "St Louis": "Saint Louis", "St. Louis": "Saint Louis", "Saint Louis Billikens": "Saint Louis",
"Saint Mary's": "Saint Mary's", "St Marys": "Saint Mary's", "St Mary's": "Saint Mary's", "Saint Marys": "Saint Mary's", "Saint Mary's Gaels": "Saint Mary's",
"Saint Peter's": "Saint Peter's", "St Peters": "Saint Peter's", "St Peter's": "Saint Peter's", "Saint Peters": "Saint Peter's", "Saint Peter's Peacocks": "Saint Peter's",
"Siena": "Siena", "Siena Saints": "Siena",
"SIU Edward": "SIU Edward", "SIU Edwardsville": "SIU Edward", "SIUE": "SIU Edward", "SIU Edwardsville Cougars": "SIU Edward",
"SMU": "SMU", "Southern Methodist": "SMU", "SMU Mustangs": "SMU",
"South Carolina": "South Carolina", "SC": "South Carolina", "South Carolina Gamecocks": "South Carolina",
"South Dakota": "South Dakota", "USD": "South Dakota", "South Dakota Coyotes": "South Dakota",
"Southern": "Southern", "Southern Univ": "Southern", "Southern University": "Southern", "Southern Jaguars": "Southern",
"Southern Miss": "Southern Miss", "Southern Mississippi": "Southern Miss", "USM": "Southern Miss", "Southern Mississippi Golden Eagles": "Southern Miss",
"St Bonaventure": "St Bonaventure", "Saint Bonaventure": "St Bonaventure", "St. Bonaventure": "St Bonaventure", "St Bonaventure Bonnies": "St Bonaventure",
"St Francis PA": "St Francis PA", "Saint Francis PA": "St Francis PA", "St. Francis (PA)": "St Francis PA", "Saint Francis University": "St Francis PA", "St Francis Red Flash": "St Francis PA",
"St John's": "St John's", "Saint John's": "St John's", "St. John's": "St John's", "St Johns": "St John's", "St John's Red Storm": "St John's",
"St Thomas": "St Thomas", "Saint Thomas": "St Thomas", "St. Thomas": "St Thomas", "St Thomas MN": "St Thomas", "St Thomas Tommies": "St Thomas",
"Stanford": "Stanford", "Stanford Cardinal": "Stanford",
"Stetson": "Stetson", "Stetson Hatters": "Stetson",
"Stonehill": "Stonehill", "Stonehill Skyhawks": "Stonehill",
"Stony Brook": "Stony Brook", "Stony Brook Seawolves": "Stony Brook",
"Syracuse": "Syracuse", "Syracuse Orange": "Syracuse",
"Tarleton St": "Tarleton St", "Tarleton State": "Tarleton St", "Tarleton Texans": "Tarleton St",
"TCU": "TCU", "Texas Christian": "TCU", "TCU Horned Frogs": "TCU",
"Temple": "Temple", "Temple Owls": "Temple",
"Tenn Tech": "Tenn Tech", "Tennessee Tech": "Tenn Tech", "Tennessee Tech Golden Eagles": "Tenn Tech",
"Tennessee": "Tennessee", "UT": "Tennessee", "Tennessee Volunteers": "Tennessee",
"Tennessee St": "Tennessee St", "Tennessee State": "Tennessee St", "Tennessee State Tigers": "Tennessee St",
"Texas": "Texas", "Texas Longhorns": "Texas",
"Texas A&M": "Texas A&M", "Texas A and M": "Texas A&M", "Texas A&M Aggies": "Texas A&M",
"Texas A&M-CC": "Texas A&M-CC", "Texas A&M Corpus Christi": "Texas A&M-CC", "Texas A&M–Corpus Christi": "Texas A&M-CC", "AMCC": "Texas A&M-CC", "Texas A&M CC Islanders": "Texas A&M-CC",
"Texas So": "Texas So", "Texas Southern": "Texas So", "TSU (Texas Southern)": "Texas So", "Texas Southern Tigers": "Texas So",
"Texas St": "Texas St", "Texas St.": "Texas St", "Texas State": "Texas St", "Texas State Bobcats": "Texas St",
"Texas Tech": "Texas Tech", "Texas Tech Red Raiders": "Texas Tech",
"The Citadel": "The Citadel", "Citadel": "The Citadel", "The Citadel Bulldogs": "The Citadel",
"Toledo": "Toledo", "Toledo Rockets": "Toledo",
"Towson": "Towson", "Towson Tigers": "Towson",
"Troy": "Troy", "Troy Trojans": "Troy",
"Tulane": "Tulane", "Tulane Green Wave": "Tulane",
"Tulsa": "Tulsa", "Tulsa Golden Hurricane": "Tulsa",
"UAB": "UAB", "Alabama Birmingham": "UAB", "UAB Blazers": "UAB",
"UC Davis": "UC Davis", "California Davis": "UC Davis", "UC Davis Aggies": "UC Davis",
"UC Irvine": "UC Irvine", "California Irvine": "UC Irvine", "UC Irvine Anteaters": "UC Irvine",
"UC Riverside": "UC Riverside", "California Riverside": "UC Riverside", "UC Riverside Highlanders": "UC Riverside",
"UCF": "UCF", "Central Florida": "UCF", "UCF Knights": "UCF",
"UCLA": "UCLA", "California Los Angeles": "UCLA", "UCLA Bruins": "UCLA",
"UConn": "UConn", "Connecticut": "UConn", "UConn Huskies": "UConn",
"UCSB": "UCSB", "UC Santa Barbara": "UCSB", "Santa Barbara": "UCSB", "UC Santa Barbara Gauchos": "UCSB",
"UCSD": "UCSD", "UC San Diego": "UCSD", "UC San Diego Tritons": "UCSD",
"UL Monroe": "UL Monroe", "Louisiana Monroe": "UL Monroe", "ULM": "UL Monroe", "Louisiana Monroe Warhawks": "UL Monroe",
"UMass": "UMass", "Massachusetts": "UMass", "UMass Minutemen": "UMass",
"UMass Lowell": "UMass Lowell", "Massachusetts Lowell": "UMass Lowell", "UMass Lowell River Hawks": "UMass Lowell",
"UMBC": "UMBC", "Maryland Baltimore County": "UMBC", "UMBC Retrievers": "UMBC",
"UNLV": "UNLV", "Nevada Las Vegas": "UNLV", "UNLV Rebels": "UNLV",
"USC": "USC", "Southern California": "USC", "USC Trojans": "USC",
"UT Arlington": "UT Arlington", "Texas Arlington": "UT Arlington", "UT Arlington Mavericks": "UT Arlington",
"UT Martin": "UT Martin", "Tennessee Martin": "UT Martin", "UT Martin Skyhawks": "UT Martin",
"UT Rio Grande": "UT Rio Grande", "UTRGV": "UT Rio Grande", "Texas Rio Grande Valley": "UT Rio Grande", "UT Rio Grande Valley Vaqueros": "UT Rio Grande",
"Utah": "Utah", "Utah Utes": "Utah",
"Utah St": "Utah St", "Utah St.": "Utah St", "Utah State": "Utah St", "Utah State Aggies": "Utah St","Utah Tech": "Utah Tech", "Dixie State": "Utah Tech", "Utah Tech Trailblazers": "Utah Tech","Utah Valley": "Utah Valley", "UVU": "Utah Valley", "Utah Valley Wolverines": "Utah Valley","UTEP": "UTEP", "Texas El Paso": "UTEP", "UTEP Miners": "UTEP","UTSA": "UTSA", "Texas San Antonio": "UTSA", "UTSA Roadrunners": "UTSA","Valparaiso": "Valparaiso", "Valpo": "Valparaiso", "Valparaiso Beacons": "Valparaiso","Vanderbilt": "Vanderbilt", "Vandy": "Vanderbilt", "Vanderbilt Commodores": "Vanderbilt","VCU": "VCU", "Virginia Commonwealth": "VCU", "VCU Rams": "VCU","Vermont": "Vermont", "Vermont Catamounts": "Vermont","Villanova": "Villanova", "Villanova Wildcats": "Villanova","Virginia": "Virginia", "Virginia Cavaliers": "Virginia","Virginia Tech": "Virginia Tech", "Va Tech": "Virginia Tech", "Virginia Tech Hokies": "Virginia Tech","VMI": "VMI", "Virginia Military Institute": "VMI", "VMI Keydets": "VMI","W Carolina": "W Carolina", "Western Carolina": "W Carolina", "Western Carolina Catamounts": "W Carolina","W Illinois": "W Illinois", "Western Illinois": "W Illinois", "Western Illinois Leathernecks": "W Illinois","W Kentucky": "W Kentucky", "Western Kentucky": "W Kentucky", "WKU": "W Kentucky", "Western Kentucky Hilltoppers": "W Kentucky","W Michigan": "W Michigan", "Western Michigan": "W Michigan", "WMU": "W Michigan", "Western Michigan Broncos": "W Michigan","Wagner": "Wagner", "Wagner Seahawks":"Wagner","Wake Forest": "Wake Forest", "Wake Forest Demon Deacons": "Wake Forest","Washington": "Washington", "Washington Huskies":"Washington","Washington St": "Washington St", "Washington St.": "Washington St","Washington State": "Washington St", "Washington State Cougars": "Washington St","Weber St": "Weber St", "Weber St.": "Weber St", "Weber State": "Weber St", "Weber State Wildcats": "Weber St","West Virginia": "West Virginia", "WVU": "West Virginia","West Virginia Mountaineers": "West Virginia","Wichita St": "Wichita St", "Wichita St.": "Wichita St", "Wichita State": "Wichita St", "Wichita State Shockers":"Wichita St","William & Mary": "William & Mary", "William and Mary": "William & Mary","William & Mary Tribe": "William & Mary","Winthrop": "Winthrop", "Winthrop Eagles":"Winthrop","Wisconsin": "Wisconsin", "Wisconsin Badgers": "Wisconsin","Wofford": "Wofford", "Wofford Terriers": "Wofford","Wright St": "Wright St","Wright St.": "Wright St", "Wright State": "Wright St","Wright State Raiders": "Wright St","Wyoming": "Wyoming", "Wyoming Cowboys": "Wyoming","Xavier": "Xavier","Xavier Musketeers": "Xavier","Yale": "Yale", "Yale Bulldogs":"Yale","Youngstown St":"Youngstown St", "Youngstown St.": "Youngstown St", "Youngstown State":"Youngstown St", "Youngstown State Penguins": "Youngstown St",}

# -----------------------------------------------------------------------------
# Helper: strip punctuation (but keep case)
# -----------------------------------------------------------------------------
_PUNCT_TRANSLATION_TABLE = str.maketrans("", "", string.punctuation)
def _strip_punctuation(text: str) -> str:
    return text.translate(_PUNCT_TRANSLATION_TABLE)
# -----------------------------------------------------------------------------
# normalize_team_name
# -----------------------------------------------------------------------------
def normalize_team_name(raw_name: str) -> str:
    """
    Normalize an incoming team name to the canonical TR spelling.

    Resolution order:
    1. TEAM_MAP_OVERRIDES (exact, case-sensitive)
    2. NORMALIZE (exact, case-sensitive)
    3. Fuzzy match (case-sensitive, punctuation-stripped, ≥ 0.90 similarity)
       against:
         - all canonical TR names (values of NORMALIZE)
         - all alias keys (keys of NORMALIZE)
    4. Fallback: return original raw_name unchanged
    """
    if raw_name is None:
        return raw_name

    # 1) Hard overrides (exact, case-sensitive)
    if raw_name in TEAM_MAP_OVERRIDES:
        return TEAM_MAP_OVERRIDES[raw_name]

    # 2) Exact alias match (case-sensitive)
    if raw_name in NORMALIZE:
        return NORMALIZE[raw_name]

    # Prepare for fuzzy matching
    # Case-sensitive, but punctuation-stripped
    stripped_input = _strip_punctuation(raw_name)

    # Build candidate set: canonical TR names + alias keys
    canonical_names = set(NORMALIZE.values())
    alias_keys = set(NORMALIZE.keys())
    candidates = canonical_names.union(alias_keys)

    best_match = None
    best_score = 0.0

    for candidate in candidates:
        stripped_candidate = _strip_punctuation(candidate)
        score = SequenceMatcher(None, stripped_input, stripped_candidate).ratio()
        if score > best_score:
            best_score = score
            best_match = candidate

    # Strict threshold: require ≥ 0.90 similarity
    if best_match is not None and best_score >= 0.90:
        # If best_match is an alias key, map through NORMALIZE
        if best_match in NORMALIZE:
            return NORMALIZE[best_match]
        # Otherwise, assume it's already a canonical TR name
        return best_match

    # 4) Fallback: return original name unchanged
    return raw_name
