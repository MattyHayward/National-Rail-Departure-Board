from textcolours import *
import json


def returnSettings(file=''):
    with open(file, 'r') as config:
        settings = json.load(config)
        return settings

def hex_to_rgb(hexcolour):
    return(tuple(int(hexcolour.lstrip('#')[i:i+2], 16) for i in (0, 2, 4)))
RGBfranchiseColour = hex_to_rgb(colour.DEFAULT)


def franchiseIdent(code='', operator=f''):
    if (code == 'LE'):
        franchiseName = f'(Greater Anglia)'
        franchiseColour = colour.GreaterAnglia
    elif (code == 'SR'):
        franchiseName = f'(ScotRail)'
        franchiseColour = colour.ScotRail
    elif (code == 'VT'):
        franchiseName = f'(Avanti West Coast)'
        franchiseColour = colour.AWC
    elif (code == 'CC'):
        franchiseName = f'(c2c)'
        franchiseColour = colour.C2C
    elif (code == 'CS'):
        franchiseName = f'(Caledonian Sleeper)'
        franchiseColour = colour.CS
    elif (code == 'CH'):
        franchiseName = f'(Chiltern Railways)'
        franchiseColour = colour.Chiltern
    elif (code == 'XC'):
        franchiseName = f'(CrossCountry)'
        franchiseColour = colour.XC
    elif (code == 'EM'):
        franchiseName = f'(East Midlands Railway)'
        franchiseColour = colour.EMR
    elif (code == 'GW'):
        franchiseName = f'(Great Western Railway)'
        franchiseColour = colour.GWR
    elif (code == 'HT'):
        franchiseName = f'(Hull Trains)'
        franchiseColour = colour.HT
    elif (code == 'GN' or code == 'TL'):
        franchiseName = f'(Thameslink)'
        franchiseColour = colour.TL
    elif (code == 'HX'):
        franchiseName = f'(Heathrow Express)'
        franchiseColour = colour.HeathExp
    elif (code == 'IL'):
        franchiseName = f'(Island Line)'
        franchiseColour = colour.ILT
    elif (code == 'AW'):
        franchiseName = f'(Transport for Wales)'
        franchiseColour = colour.TFW
    elif (code == 'LN'):
        franchiseName = f'(London Northwestern Railways)'
        franchiseColour = colour.LNW
    elif (code == 'GR'):
        franchiseName = f'(London North Eastern Railway)'
        franchiseColour = colour.LNE
    elif (code == 'NT'):
        franchiseName = f'(Northern Trains)'
        franchiseColour = colour.NT
    elif (code == 'SN'):
        franchiseName = f'(Southern)'
        franchiseColour = colour.Southern
    elif (code == 'SE'):
        franchiseName = f'(Southeastern)'
        franchiseColour = colour.Southeastern
    elif (code == 'SW'):
        franchiseName = f'(South Western Railway)'
        franchiseColour = colour.SWR
    elif (code == 'SX'):
        franchiseName = f'(Stansted Express)'
        franchiseColour = colour.StanExp
    elif (code == 'TP'):
        franchiseName = f'(TransPennine Express)'
        franchiseColour = colour.TPX
    elif (code == 'LM'):
        franchiseName = f'({operator})'
        franchiseColour = colour.WMT
    elif (code == 'EU' or code == 'ES'):
        franchiseName = f'(Eurostar)'
        franchiseColour = colour.EURO
    elif (code == 'GC'):
        franchiseName = f'(Grand Central)'
        franchiseColour = colour.GrandCentral
    elif (code == 'HC'):
        franchiseName = f'(Heathrow Connect)'
        franchiseColour = colour.HeathCon
    elif (code == 'NY'):
        franchiseName = f'(North Yorkshire Moors Railway)'
        franchiseColour = colour.YorkMoor
    elif (code == 'WR'):
        franchiseName = f'(West Coast Railways)'
        franchiseColour = colour.WCR
    elif (code == 'LD'):
        franchiseName = f'(Lumo)'
        franchiseColour = colour.ECT
    elif (code == 'LF'):
        franchiseName = f'(Grand Union)'
        franchiseColour = colour.GU
    elif (code == 'LO'):
        franchiseName = f'(London Overground)'
        franchiseColour = colour.LO
    elif (code == 'LS'):
        franchiseName = f'(Locomotive Services)'
        franchiseColour = colour.DEFAULT
    elif (code == 'LT'):
        franchiseName = f'(London Underground)'
        franchiseColour = colour.DEFAULT
    elif (code == 'ME'):
        franchiseName = f'(Merseyrail)'
        franchiseColour = colour.DEFAULT
    elif (code == 'XR'):
        franchiseName = f'(Elizabeth Line)'
        franchiseColour = colour.ELIZ
    elif (len(code) > 0):
        franchiseName = f'({operator})'
        franchiseColour = colour.DEFAULT
    else:
        franchiseName = f''
        franchiseColour = colour.DEFAULT

    return franchiseName, franchiseColour


def replaceStationName(destination = f''):
    if (destination == f'Adlington (Cheshire)'):
        return f'Adlington'
    elif (destination == f'Adlington (Lancashire)'):
        return f'Adlington'
    elif (destination == f'Ardrossan South Beach'):
        return f'Ardrossan Sth Beach'
    elif (destination == f'Ascott-under-Wychwood'):
        return f'Ascott-u-Wychwood'
    elif (destination == f'Ashurst (Kent)'):
        return f'Ashurst'
    elif (destination == f'Ashurst (New Forest)'):
        return f'Ashurst'
    elif (destination == f'Aylesbury Vale Parkway'):
        return f'Aylesbury Vale Pkwy'
    elif (destination == f'Beckenham Junction'):
        return f'Beckenham Jctn'
    elif (destination == f'Belfast Great Victoria Street'):
        return f'Belfast Gt Vic St'
    elif (destination == f'Belfast Lanyon Place'):
        return f'Belfast Lanyon Pl'
    elif (destination == f'Bentley (Hampshire)'):
        return f'Bentley'
    elif (destination == f'Bentley (South Yorkshire)'):
        return f'Bentley'
    elif (destination == f'Berwick-upon-Tweed'):
        return f'Berwick-u-Tweed'
    elif (destination == f'Birkenhead Hamilton Square'):
        return f"Birkenhead Hmltn Sq"
    elif (destination == f'Birmingham International'):
        return f'Birmingham Intl'
    elif (destination == f'Birmingham Moor Street'):
        return f'Birmingham Moor St'
    elif (destination == f'Birmingham New Street'):
        return f'Birmingham New St'
    elif (destination == f'Blackpool Pleasure Beach'):
        return f'Blackpool Plsre Beach'
    elif (destination == f'Blundellsands & Crosby'):
        return f'Blndllsnds & Crsby'
    elif (destination == f'Borough Green & Wrotham'):
        return f"Borough Grn & W'ham"
    elif (destination == f'Box Hill & Westhumble'):
        return f"Box Hill & W'hmble"
    elif (destination == f"Bradford Forster Square"):
        return f"Bradford Forster Sq"
    elif (destination == f"Bramley (Hampshire)"):
        return f"Bramley"
    elif (destination == f"Bramley (West Yorkshire)"):
        return f"Bramley"
    elif (destination == f"Brampton (Cumbria)"):
        return f"Brampton"
    elif (destination == f"Brampton (Suffolk)"):
        return f"Brampton"
    elif (destination == f"Bristol Temple Meads"):
        return f"Bristol Temple Meads"
    elif (destination == f"Brondesbury Park"):
        return f"Brondesbury Pk"
    elif (destination == f"Buckshaw Parkway"):
        return f"Buckshaw Pkway"
    elif (destination == f"Burnham (Buckinghamshire)"):
        return f"Burnham"
    elif (destination == f"Burnley Manchester Road"):
        return f"Burnley Man'ter Rd"
    elif (destination == f"Burscough Junction"):
        return f"Burscough Jctn"
    elif (destination == f"Caledonian Road and Barnsbury"):
        return f"Caledonian Rd"
    elif (destination == f"Cardiff Queen Street"):
        return f"Cardiff Queen St"
    elif (destination == f"Carshalton Beeches"):
        return f"Carshalton Bchs"
    elif (destination == f"Chafford Hundred Lakeside"):
        return f"Chafford H L'side"
    elif (destination == f"Chapelton (Devon)"):
        return f"Chapelton"
    elif (destination == f"Chapeltown (Yorkshire)"):
        return f"Chapeltown"
    elif (destination == f"Chappel and Wakes Colne"):
        return f"Chappel & Wakes C"
    elif (destination == f"Chessington North"):
        return f"Chessington Nth"
    elif (destination == f"Chessington South"):
        return f"Chessington Sth"
    elif (destination == f"Chestfield & Swalecliffe"):
        return f"Chestfield & S'cliffe"
    elif (destination == f"Church and Oswaldtwistle"):
        return f"Church & O'twistle"
    elif (destination == f"Clapham High Street"):
        return f"Clapham High St"
    elif (destination == f"Clarbeston Road"):
        return f"Clarbeston Rd"
    elif (destination == f"Coatbridge Sunnyside"):
        return f"Coatbridge S'side"
    elif (destination == f"Cobham & Stoke d'Abernon"):
        return f"Cobham & S d'Abernon"
    elif (destination == f"Coombe Junction Halt"):
        return f"Coombe Junction Hlt"
    elif (destination == f"Dunfermline Queen Margaret"):
        return f"Dunfermline Q Mgt"
    elif (destination == f"East Midlands Parkway"):
        return f"East Midlands Pkway"
    elif (destination == f"Ebbsfleet International"):
        return f"Ebbsfleet Intl"
    elif (destination == f"Ebbw Vale Parkway"):
        return f"Ebbw Vale Pkway"
    elif (destination == f"Elstree & Borehamwood"):
        return f"Elstree & B'hamwood"
    elif (destination == f"Energlyn and Churchill Park"):
        return f"Energlyn & C'hill Pk"
    elif (destination == f"Euxton Balshaw Lane"):
        return f"Euxton Balshaw Ln"
    elif (destination == f"Finchley Road & Frognal"):
        return f"Finchley Rd & F'nal"
    elif (destination == f"Fishguard and Goodwick"):
        return f"Fishguard & G'wick"
    elif (destination == f"Gainsborough Central"):
        return f"Gainsborough Ctl"
    elif (destination == f"Gainsborough Lea Road"):
        return f"Gainsborough L Rd"
    elif (destination == f"Garth (Mid Glamorgan)"):
        return f"Garth"
    elif (destination == f"Garth (Powys)"):
        return f"Garth"
    elif (destination == f"Georgemas Junction"):
        return f"Georgemas Jctn"
    elif (destination == f"Gillingham (Dorset)"):
        return f"Gillingham"
    elif (destination == f"Gillingham (Kent)"):
        return f"Gillingham"
    elif (destination == f"Glasgow Queen Street"):
        return f"Glasgow Q St"
    elif (destination == f"Glenrothes with Thornton"):
        return f"Glenrothes w T'ton"
    elif (destination == f"Great Victoria Street"):
        return f"Great Victoria St"
    elif (destination == f"Haddenham and Thame Parkway"):
        return f"Had'ham & Thame Pky"
    elif (destination == f"Harringay Green Lanes"):
        return f"Harringay Grn Lns"
    elif (destination == f"Harrow & Wealdstone"):
        return f"Harrow & W'stone"
    elif (destination == f"Harwich International"):
        return f"Harwich Intl"
    elif (destination == f"Hatfield and Stainforth"):
        return f"Hatfield & S'forth"
    elif (destination == f"Hayes and Harlington"):
        return f"Hayes & H'lington"
    elif (destination == f"Heathrow Terminals 1, 2 and 3"):
        return f"Heathrow T2&3"
    elif (destination == f"Heathrow Terminal 4"):
        return f"Heathrow T4"
    elif (destination == f"Heathrow Terminal 5"):
        return f"Heathrow T5"
    elif (destination == f"Helensburgh Central"):
        return f"Helensburgh Cntl"
    elif (destination == f"Highbridge and Burnham"):
        return f"Highbridge & B'ham"
    elif (destination == f"Highbury and Islington"):
        return f"Highbury & Islington"
    elif (destination == f"Hoveton and Wroxham"):
        return f"Hoveton & W'ham"
    elif (destination == f"James Cook University Hospital"):
        return f"J Cook Uni Hospital"
    elif (destination == f"Kempston Hardwick"):
        return f"Kempston H'wick"
    elif (destination == f"Kirkham and Wesham"):
        return f"Kirkham & Wesham"
    elif (destination == f"Langwith-Whaley Thorns"):
        return f"Langwith-Whaley T"
    elif (destination == f"Lazonby and Kirkoswald"):
        return f"Lazonby & K'wald"
    elif (destination == f"Letchworth Garden City"):
        return f"Letchworth Gden City"
    elif (destination == f"Leyton Midland Road"):
        return f"Leyton Midland Rd"
    elif (destination == f"Leytonstone High Road"):
        return f"Leytonstone H Rd"
    elif (destination == f"Lichfield Trent Valley"):
        return f"Lichfield T Valley"
    elif (destination == f"Lisvane and Thornhill"):
        return f"Lisvane & T'hill"
    elif (destination == f"Liverpool James Street"):
        return f"Liverpool James St"
    elif (destination == f"Liverpool Lime Street"):
        return f"Liverpool Lime St"
    elif (destination == f"Liverpool South Parkway"):
        return f"Liverpool Sth Pkway"
    elif (destination == f"Llandudno Junction"):
        return f"Llandudno Jctn"
    elif (destination == f"Loch Eil Outward Bound"):
        return f"Loch Eil Outbound"
    elif (destination == f"London Fenchurch Street"):
        return f"London Fenchurch St"
    elif (destination == f"London Liverpool Street"):
        return f"London Liverpool St"
    elif (destination == f"London Road (Brighton)"):
        return f"London Road"
    elif (destination == f"London Road (Guildford)"):
        return f"London Road"
    elif (destination == f"London St Pancras International"):
        return f"London St Pancras"
    elif (destination == f"London Waterloo East"):
        return f"London Waterloo East"
    elif (destination == f"Loughborough Junction"):
        return f"Loughborough Jctn"
    elif (destination == f"Luton Airport Parkway"):
        return f"Luton Airport Pkway"
    elif (destination == f"Lympstone Commando"):
        return f"Lympstone Cmmdo"
    elif (destination == f"Maesteg Ewenny Road"):
        return f"Maesteg E Road"
    elif (destination == f"Manchester Oxford Road"):
        return f"Manchester Ox Rd"
    elif (destination == f"Manchester Piccadilly"):
        return f"Manchester Piccadilly"
    elif (destination == f"Manchester United Football Ground"):
        return f"Man U Football Grd"
    elif (destination == f"Manchester Victoria"):
        return f"Manchester Victoria"
    elif (destination == f"Mansfield Woodhouse"):
        return f"Mansfield W'house"
    elif (destination == f"Milton Keynes Central"):
        return f"Milton Keynes Cntl"
    elif (destination == f"Mottisfont & Dunbridge"):
        return f"Mottisfont & Dbrdge"
    elif (destination == f"Nailsea and Backwell"):
        return f"Nailsea and B'well"
    elif (destination == f"Northumberland Park"):
        return f"Northumberland Pk"
    elif (destination == f"Oulton Broad North"):
        return f"Oulton Broad Nth"
    elif (destination == f"Oulton Broad South"):
        return f"Oulton Broad Sth"
    elif (destination == f"Oxenholme Lake District"):
        return f"Oxenholme L Dst"
    elif (destination == f"Paisley Gilmour Street"):
        return f"Paisley G'mour St"
    elif (destination == f"Pembrey and Burry Port"):
        return f"Pembrey & Burry Pt"
    elif (destination == f"Pevensey and Westham"):
        return f"Pevensey & Westham"
    elif (destination == f"Pontypool and New Inn"):
        return f"Pontypool & New Inn"
    elif (destination == f"Possilpark and Parkhouse"):
        return f"Possilpark & P'house"
    elif (destination == f"Prestwick International Airport"):
        return f"Prestwick Airport"
    elif (destination == f"Queens Park (Glasgow)"):
        return f"Queens Park"
    elif (destination == f"Queens Park (London)"):
        return f"Queens Park"
    elif (destination == f"Rainham (London)"):
        return f"Rainham"
    elif (destination == f"Rainham (Kent)"):
        return f"Rainham"
    elif (destination == f"Ramsgreave and Wilpshire"):
        return f"Ramsgreave & W'shire"
    elif (destination == f"Reedham (Norfolk)"):
        return f"Reedham"
    elif (destination == f"Reedham (Surrey)"):
        return f"Reedham"
    elif (destination == f"Rhoose Cardiff International Airport"):
        return f"Rhoose Cardiff Arpt"
    elif (destination == f"Risca and Pontymister"):
        return f"Risca & Pontymister"
    elif (destination == f"Rugeley Trent Valley"):
        return f"Rugeley T Valley"
    elif (destination == f"Ryde St John's Road"):
        return f"Ryde St John's Rd"
    elif (destination == f"St Annes-on-the-Sea"):
        return f"St Annes-o-t-Sea"
    elif (destination == f"St Budeaux Ferry Road"):
        return f"St Budeaux Ferry Rd"
    elif (destination == f"St Budeaux Victoria Road"):
        return f"St Budeaux Vic Rd"
    elif (destination == f"St Keyne Wishing Well Halt"):
        return f"St Keyne W W Halt"
    elif (destination == f"St Leonards Warrior Square"):
        return f"St Leonards W Sq"
    elif (destination == f"Sandal and Agbrigg"):
        return f"Sandal & Agbrigg"
    elif (destination == f"Sandwell and Dudley"):
        return f"Sandwell & Dudley"
    elif (destination == f"Seaforth and Litherland"):
        return f"Seaforth & Litherland"
    elif (destination == f"Severn Tunnel Junction"):
        return f"Severn Tunnel Jctn"
    elif (destination == f"Shoreditch High Street"):
        return f"Shoreditch H St"
    elif (destination == f"Smallbrook Jnct"):
        return f"Adlington"
    elif (destination == f"Smethwick Galton Bridge"):
        return f"Smethwick G Bridge"
    elif (destination == f"Smethwick Rolfe Street"):
        return f"Smethwick Rolfe St"
    elif (destination == f"South Woodham Ferrers"):
        return f"Sth Woodham Ferrers"
    elif (destination == f"Southampton Airport Parkway"):
        return f"S'ton Airport Pkway"
    elif (destination == f"Southampton Central"):
        return f"Southampton Cntl"
    elif (destination == f"Stanlow and Thornton"):
        return f"Stanlow & Thornton"
    elif (destination == f"Stansted Mountfitchet"):
        return f"Stansted M'fitchet"
    elif (destination == f"Steeton and Silsden"):
        return f"Steeton & Silsden"
    elif (destination == f"Stourbridge Junction"):
        return f"Stourbridge Jnct"
    elif (destination == f"Stratford International"):
        return f"Stratford Intl"
    elif (destination == f"Stratford-upon-Avon Parkway"):
        return f"S'ford-u-Avon Pkway"
    elif (destination == f"Stratford-upon-Avon"):
        return f"Stratford-u-Avon"
    elif (destination == f"Sudbury & Harrow Road"):
        return f"Sudbury & Harrow Rd"
    elif (destination == f"Sutton (London)"):
        return f"Sutton"
    elif (destination == f"Tame Bridge Parkway"):
        return f"Tame Bridge Pkway"
    elif (destination == f"Tutbury and Hatton"):
        return f"Tutbury & Hatton"
    elif (destination == f"Upper Warlingham"):
        return f"Upper W'lingham"
    elif (destination == f"Wallasey Grove Road"):
        return f"Wallasey Grove Rd"
    elif (destination == f"Walthamstow Central"):
        return f"Walthamstow Cntl"
    elif (destination == f"Walthamstow Queens Road"):
        return f"Walthamstow Q Rd"
    elif (destination == f"Walton (Merseyside)"):
        return f"Walton"
    elif (destination == f"Warrington Bank Quay"):
        return f"Warrington Bank Quay"
    elif (destination == f"Waterloo (Merseyside)"):
        return f"Waterloo"
    elif (destination == f"Watford High Street"):
        return f"Watford High St"
    elif (destination == f"Wavertree Technology Park"):
        return f"Wavertree Tech Pk"
    elif (destination == f"Wellington Shropshire"):
        return f"Wellington S'shire"
    elif (destination == f"West Hampstead Thameslink"):
        return f"West H'stead T'link"
    elif (destination == f"Whittlesford Parkway"):
        return f"Whittlesford Pkwy"
    elif (destination == f"Wigan North Western"):
        return f"Wigan Nth Western"
    elif (destination == f"Windsor and Eton Central"):
        return f"Windsor & Eton Cntl"
    elif (destination == f"Windsor and Eton Riverside"):
        return f"Windsor & Eton R'side"
    elif (destination == f"Worcester Foregate Street"):
        return f"Worcester Foregate St"
    elif (destination == f"Worcestershire Parkway"):
        return f"W'stershire Pkwy"
    elif (destination == f"Worcester Shrub Hill"):
        return f"Worcester Shrub Hill"
    else:
        return destination