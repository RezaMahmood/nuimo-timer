#!/usr/bin/env python

import pyfiglet

class Display(object):
    def __init__(self):
        self.paddedRow = "         "

    def singleChar(self, char, font):        
        validFonts = ValidFonts()
        # Validate the font
        if font in dir(validFonts):
            if len(char) > 2:
                raise ValueError("%s is not a valid character. Characters must have length == 1" % char)
            else:
                fontType = getattr(validFonts, font)
                if len(char) == 2:
                    figlet = pyfiglet.Figlet("clr8x8")
                else:
                    figlet = pyfiglet.Figlet(fontType["name"])
                text = figlet.renderText(char)
                text = self.MakeClean(str(text), fontType)
                return text
        else:
            raise ValueError("%s is not a valid font.  Only fonts defined in ValidFonts can be used" % font)

    def icon(self, iconName):
        icons = {
                "start":"           ***      ****     *****    ******   *****    ****     ***             ",
                "pause":"          *** ***  *** ***  *** ***  *** ***  *** ***  *** ***  *** ***          ",              
                "1":"             *       **        *        *        *        *       ***            ",
                "2":"            ***         *        *       *       *       *        ****           ",
                "3":"            **      *  *        *       *         *     *  *      **             ",
                "4":"           *        *        * *      * *      ****       *       ***            ",
                "5":"           ****     *        *        ****        *        *     ****            ",
                "6":"           ****     *        *        ****     *  *     *  *     ****            ",
                "7":"           ****        *       *       **       *        *        *              ",
                "8":"",
                "9":"",
                "10":"           *  **   ** *  *   * *  *   * *  *   * *  *   * *  *  *** **           ",
                "11":"           *   *   **  **    *   *    *   *    *   *    *   *   *** ***          ",
                "12":"          *  ***  **     *  *     *  *    *   *   *    *  *    *** ****          ",
                "13":"          *   **  **  *  *  *     *  *    *   *     *  *  *  * ***  **           ",
                "14":"          *  *    **  *     *  * *   *  * *   *  ****  *    *  ***  ***          ",
                "15":"          *  **** **  *     *  *     *  ****  *     *  *     * *** ****          ",
                "16":"          *  **** **  *     *  *     *  ****  *  *  *  *  *  * *** ****          ",
                "17":"          *  **** **     *  *    *   *   **   *   *    *   *   ***  *            ",
                "18":"          *  **** **  *  *  *  *  *  *   **   *  *  *  *  *  * *** ****          ",
                "19":"          *  **** **  *  *  *  *  *  *  ****  *     *  *     * *** ****          ",
                "20":"         ***   **    * *  *   * *  *  *  *  * *   *  **    *  *****  **          ",
                "21":"         ***   *     * **     *  *    *   *   *    *  *     *  **** ***          ",
                "22":"         ***  ***    *    *   *    *  *    *  *    *  *    *   **** ****         ",
                "23":"         ***   **    * *  *   *    *  *    *  *      **    *  *****  **          ",
                "24":"         ***  *      * *      * * *   *  * *  *   *****      * ****  ***         ",
                "25":"         ***  ****   * *      * *     *  **** *      **       ***** ****         ",
                "26":"         ***  ****   * *      * *     *  **** *   *  **    *  ***** ****         ",
                "27":"         ***  ****   *    *   *   *   *   **  *    *  *     *  ****  *           ",
                "28":"         ***  ****   * *  *   * *  *  *   **  *   *  **    *  ***** ****         ",
                "29":"         ***  ****   * *  *   * *  *  *  **** *      **       ***** ****         ",
                "30":"",
                "31":"",
                "32":"",
                "88":"          **   ** *  * *  **  * *  * **   ** *  * *  **  * *  * **   **          "
            }
        
        return icons[iconName]
        

    def MakeClean(self, text, fontType):
        # Clean the output from figlet into something Nuimo can use          
        amountOfPadding = 9 - fontType["height"]
        text = text.replace(fontType["char"],"*")
        print("attempting to print:\n\n" + str(text))
        text = text.replace("\n","")
        #if amountOfPadding > 0:
        #    for padding in range(0, amountOfPadding):
        #        text = self.paddedRow + text

        print ("actually printing:\n\n" + text)
        return text    

    
class ValidFonts(object):
    def __init__(self):
        self.taxi = {"name":"taxi____", "char":"#","height":7}
        self.clb8x8 = {"name":"clb8x8","char":"#","height":8}
        self.sansi = {"name":"sansi_2","char":"#","height":6}
        self.clr8x8 = {"name":"clr8x8","char":"#","height":8}

       