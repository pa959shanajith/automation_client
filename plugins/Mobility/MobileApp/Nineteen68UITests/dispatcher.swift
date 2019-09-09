//
//  dispatcher.swift
//  UI Tests
//
//  Created by Nayak Dheeraj on 08/08/18.
//  Copyright © 2018 Nineteen68. All rights reserved.
//

import Foundation
import XCTest

class dispatch {
    
    func get_value(bundle_id:String,action:String,label:String="",key:String="",input_text:String="",forDuration:TimeInterval=0,key2:String="",label2:String="",float_val:Float=0) -> (String) {
        var maindict:[String:XCUIElementQuery] =
            ["Button":XCUIApplication(bundleIdentifier:bundle_id).buttons,
             "statictexts":XCUIApplication(bundleIdentifier:bundle_id).staticTexts,
             "image":XCUIApplication(bundleIdentifier:bundle_id).images,
             "RadioButton":XCUIApplication(bundleIdentifier:bundle_id).radioButtons,
             "get_datepicker":XCUIApplication(bundleIdentifier:bundle_id).datePickers,
             "links":XCUIApplication(bundleIdentifier:bundle_id).links,
             "XCUIElementTypeSecureTextField":XCUIApplication(bundleIdentifier:bundle_id).secureTextFields,
             "EditText":XCUIApplication(bundleIdentifier:bundle_id).textFields,
             "CheckBox":XCUIApplication(bundleIdentifier:bundle_id).checkBoxes,
             "get_maps":XCUIApplication(bundleIdentifier:bundle_id).maps,
             "otherElements":XCUIApplication(bundleIdentifier: bundle_id).otherElements,
             "cells":XCUIApplication(bundleIdentifier: bundle_id).cells,
             "XCUIElementTypeSearchField":XCUIApplication(bundleIdentifier: bundle_id).searchFields,
             "keys":XCUIApplication(bundleIdentifier: bundle_id).keys,
             "switches":XCUIApplication(bundleIdentifier: bundle_id).switches,
             "XCUIElementTypeSlider":XCUIApplication(bundleIdentifier: bundle_id).sliders,
             "activityIndicators":XCUIApplication(bundleIdentifier: bundle_id).activityIndicators,
             "progressIndicators":XCUIApplication(bundleIdentifier: bundle_id).progressIndicators,
             "textViews":XCUIApplication(bundleIdentifier: bundle_id).textViews,
             "XCUIElementTypePickerWheel":XCUIApplication(bundleIdentifier: bundle_id).pickerWheels,
             "empty":XCUIApplication(bundleIdentifier: bundle_id).mattes
        ]
        
        
        switch action {
        case "doubletap":return performing_guestures().doubletap(querytype: maindict[key]!, label: label)
        case "adjusting_Slider":return performing_guestures().adjusting_Slider(querytype: maindict[key]!, label: label, set_to: CGFloat(float_val))
        case "type_text":return type_box_operations().type_text(bundle_id: bundle_id, querytype: maindict[key]!, label: label, input: input_text)
        case "type_securetext":return type_box_operations().type_securetext(bundle_id: bundle_id, querytype: maindict[key]!, label: label, input: input_text)
        case "tap": return performing_guestures().tap(querytype: maindict[key]!, label: label)
        case "longpress":return performing_guestures().long_press(querytype: maindict[key]!, label: label, forDuration: forDuration)
        case "getbuttonname": return verify().getbuttonname(label: label,querytype: maindict[key]!)
        case "verifybuttonname": return verify().verify_buttonname(label: label , input: input_text , querytype: maindict[key]!)
        case "verifyelementexists":return verify().verify_elementexists(bundle_id: bundle_id, label: label, querytype: maindict[key]!)
        case "verifydoesnotelementexists":return verify().verify_elemendoesnottexists(bundle_id: bundle_id, label: label, querytype: maindict[key]!)
        case "verifyelementenabled":return verify().verify_elementenabled(bundle_id: bundle_id, label: label, querytype: maindict[key]!)
        case "verifyelementdisabled":return verify().verify_elementdisabled(bundle_id: bundle_id, label: label, querytype: maindict[key]!)
        case "selectradiobutton": return performing_guestures().select_radio_checkbox(querytype: maindict[key]!, label: label)
        case "getstatus": return performing_guestures().get_status(querytype: maindict[key]!, label: label)
        case "unselectcheckbox": return performing_guestures().unselect_checkbox(querytype: maindict[key]!, label: label)
        case "backpress": return run_and_kill().backpress()
        case "swipeup":return performing_guestures().swipe_up(querytype: maindict[key]!, label: label)
        case "swipedown":return performing_guestures().swipe_down(querytype: maindict[key]!, label: label)
        case "swipeleft":return performing_guestures().swipe_left(querytype: maindict[key]!, label: label)
        case "swiperight":return performing_guestures().swipe_right(querytype: maindict[key]!, label: label)
        case "cleartext":return type_box_operations().cleartext(bundle_id: bundle_id, querytype:  maindict[key]!, label: label)
        case "gettext":return type_box_operations().gettext(bundle_id: bundle_id, querytype:  maindict[key]!, label: label)
        case "waitforelementexists":return verify().wait_for_elementexists(bundle_id: bundle_id, label: label, querytype: maindict[key]!)
        case "verifyhidden":return verify().verify_hidden(bundle_id: bundle_id, label: label, querytype:  maindict[key]!)
        case "verifyvisible":return verify().verify_visible(bundle_id: bundle_id, label: label, querytype:  maindict[key]!)
        case "LaunchApplication":return run_and_kill().App_Launch(bundle_id: bundle_id)
        case "closeapplication":return run_and_kill().close_application(bundle_id: bundle_id)
        case "setvalue": return performing_guestures().set_value(querytype: maindict[key]!, label: label, input: input_text)
        case "getvalue": return performing_guestures().get_value(querytype: maindict[key]!, label: label)
        case "verifytext": return verify().verify_text(bundle_id: bundle_id, label: label, querytype: maindict[key]!, input: input_text)

        
        default:
            errrorhandle().send_error(message: "keyword is not supported")
            return "fail"
        }
    return "pass"
    
}


}
