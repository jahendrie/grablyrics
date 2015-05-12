#!/usr/bin/env python
#===============================================================================
#   grablyrics.py   |   version 1.0     |   zlib license    |   2015-05-12
#   James Hendrie                       |   hendrie.james@gmail.com
#
#   Description:
#       This script grabs a page from the Lyrics Wiki (lyrics.wikia.com),
#       decodes the page and prints the decoded lyrics to the terminal.
#===============================================================================
import sys


def format_string( oldString ):
    """
    This function turns a given string (one of the two arguments passed to the
    script by the user) into one that can be used as part of the URL used to
    fetch the page from the lyrics wiki.  Specifically, it needs to be camel-
    case (or 'title' case) with underscores replacing spaces.
    """
    string = oldString.title()
    return( string.replace( ' ', '_', -1 ) )



def print_usage():
    print( "Usage:  grablyrics \"BAND_NAME\" \"SONG NAME\"" )


def print_help():
    print_usage()
    print( "" )
    print( "This script fetches lyrics from the Lyrics Wiki (lyrics.wikia.com)")
    print( "and prints them to your terminal.")
    print( "\nExamples:" )
    print( "  grablyrics \"between the buried and me\" \"informal gluttony\"" )
    print( "  grablyrics 'radiohead' 'street spirit'" )


def print_error():
    print( "ERROR:  Incorrect usage" )
    print_usage()


def get_page( URL ):
    
    ##  If they're using Python 3
    if sys.version[0] == '3':
        import urllib.request
        rawPage = urllib.request.urlopen( URL )
        page = rawPage.read().decode()
        return( page )

    ##  If they're using Python 2
    elif sys.version[0] == '2':
        import urllib
        rawPage = urllib.urlopen( URL )
        page = rawPage.read()
        return( page )

def main():
    ##  Check for the proper number of arguments
    if len( sys.argv ) != 3:
        if len( sys.argv ) == 2:
            if sys.argv[1] == "-h" or sys.argv[1] == "--help":
                print_help()
                sys.exit( 0 )
        else:
            print_error()
            sys.exit( 1 )

    ##  First arg is the band name, second is the title of the track
    band = format_string( sys.argv[ 1 ] )
    song = format_string( sys.argv[ 2 ] )

    ##  We're using the lyrics wiki
    baseSite = "http://lyrics.wikia.com"

    ##  Get the web page
    page = get_page( "%s/%s:%s" % ( baseSite, band, song ))

    ##  The first and second tokens for partitioning
    t1 = r"insertBefore(r,s)};}})();</script>"
    t2 = "<!--"

    ##  Grab the lyrics, which are encoded in octal
    octLyrics = page.partition( t1 )[2].partition( t2 )[0]
    lyrics = octLyrics.replace( "&#", '', -1 )
    lyrics = lyrics.replace( "<br />", "10;", -1 ).split( ';' )

    ##  Go through the lyric character octals, converting them to ascii
    ##  characters and adding them all to one long lyrics string
    lyricString = ""
    for c in lyrics:
        if c != '':
            lyricString += ( "%c" % int( c ))


    ##  Print the band name, title of the song and lyrics sheet
    print( sys.argv[1].title() )
    print( sys.argv[2].title() )
    print( "" )
    print( lyricString )



if __name__ == "__main__":
    main()
