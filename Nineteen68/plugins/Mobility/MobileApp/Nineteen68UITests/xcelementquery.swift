//
//  xcelementquery.swift
//  UI Tests
//
//  Created by Nayak Dheeraj on 08/08/18.
//  Copyright © 2018 Nineteen68. All rights reserved.
//


import Foundation
import XCTest


class xcelement_query {
    
    
    
    func dispatch(bundle_id: String,querytype:[String]) -> Array<Any> {

        var maindict:[String:XCUIElementQuery] =
            ["Button":XCUIApplication(bundleIdentifier:bundle_id).buttons,
             "statictexts":XCUIApplication(bundleIdentifier:bundle_id).staticTexts,
             "image":XCUIApplication(bundleIdentifier:bundle_id).images,
             "RadioButton":XCUIApplication(bundleIdentifier:bundle_id).radioButtons,
             "get_datepicker":XCUIApplication(bundleIdentifier:bundle_id).datePickers,
             "links":XCUIApplication(bundleIdentifier:bundle_id).links,
             "EditText":XCUIApplication(bundleIdentifier:bundle_id).textFields,
             "XCUIElementTypeSecureTextField":XCUIApplication(bundleIdentifier:bundle_id).secureTextFields,
             "CheckBox":XCUIApplication(bundleIdentifier:bundle_id).checkBoxes,
             "get_maps":XCUIApplication(bundleIdentifier:bundle_id).maps,
             "otherElements":XCUIApplication(bundleIdentifier: bundle_id).otherElements,
             "XCUIElementTypeSearchField":XCUIApplication(bundleIdentifier: bundle_id).searchFields,
             "keys":XCUIApplication(bundleIdentifier: bundle_id).keys,
             "switches":XCUIApplication(bundleIdentifier: bundle_id).switches,
             "XCUIElementTypeSlider":XCUIApplication(bundleIdentifier: bundle_id).sliders,
             "activityIndicators":XCUIApplication(bundleIdentifier: bundle_id).activityIndicators,
             "progressIndicators":XCUIApplication(bundleIdentifier: bundle_id).progressIndicators,
             "textViews":XCUIApplication(bundleIdentifier: bundle_id).textViews,
             "cells":XCUIApplication(bundleIdentifier: bundle_id).cells,
             "XCUIElementTypePickerWheel":XCUIApplication(bundleIdentifier: bundle_id).pickerWheels]
       

        
        var array = [Any]()
        for type in querytype{
            var label = ""
            if maindict[type] != nil {
                for i in 0..<maindict[type]!.count{
                    if  maindict[type]!.element(boundBy: i).exists{
                    label = maindict[type]!.element(boundBy: i).label
                    var dict = [ String : Any ]()
                    dict["tag"] = type
                    dict["custname"] = label
                    if label != "" {dict["xpath"] = label+"&$#"+type}
                    else{dict["xpath"] = "bound"+String(i) + "&$#"+type}
                    if  type == "cells" || type == "links" || type == "CheckBox" || type == "Button" || type == "switches" || type == "XCUIElementTypeSlider" || type == "activityIndicators" || type == "progressIndicators" || type == "XCUIElementTypeSearchField" || type == "EditText" || type == "XCUIElementTypeSecureTextField" ||  type == "image" || type == "textViews" || type == "XCUIElementTypePickerWheel"{
                            
                        
                        let screenshot = XCUIScreen.main.screenshot()
                        let screenshot_image = screenshot.image
                        dict["height"] = maindict[type]!.element(boundBy: i).frame.size.height * screenshot_image.scale
                        dict["width"] =  maindict[type]!.element(boundBy: i).frame.size.width * screenshot_image.scale
                        dict["top"] =  maindict[type]!.element(boundBy: i).frame.origin.y * screenshot_image.scale
                        dict["left"] =  maindict[type]!.element(boundBy: i).frame.origin.x * screenshot_image.scale
                        dict["reference"] = ""
                        dict["text"] = "ios"
                        dict["enabled"] = "true"
                        dict["id"] = ""
                        dict["tempId"] = ""
                        if label != ""{
                            array.append(dict)
                        }
                        else{
                            dict["tag"] = type
                            dict["custname"] = maindict[type]!.element(boundBy: i).value
                            if dict["custname"] as! String == ""{
                                dict["custname"]="No name "+String(i)
                            }
                            dict["xpath"] = "bound"+String(i) + "&$#"+type
                            array.append(dict)
                            
                            }
                        
                    }
                    else if type == "statictexts"{
                        if label != ""{
                            if label.count <= 50{
                                let screenshot = XCUIScreen.main.screenshot()
                                let screenshot_image = screenshot.image
                                dict["height"] = maindict[type]!.element(boundBy: i).frame.size.height * screenshot_image.scale
                                dict["width"] = maindict[type]!.element(boundBy: i).frame.size.width * screenshot_image.scale
                                dict["top"] = maindict[type]!.element(boundBy: i).frame.origin.y * screenshot_image.scale
                                dict["left"] = maindict[type]!.element(boundBy: i).frame.origin.x * screenshot_image.scale
                                dict["reference"] = ""
                                dict["text"] = "ios"
                                dict["enabled"] = "true"
                                dict["id"] = ""
                                dict["tempId"] = ""
                                array.append(dict)
                            }
                            else{
                                let screenshot = XCUIScreen.main.screenshot()
                                let screenshot_image = screenshot.image
                                dict["xpath"] = "bound"+String(i) + "&$#"+type
                                dict["height"] = maindict[type]!.element(boundBy: i).frame.size.height * screenshot_image.scale
                                dict["width"] = maindict[type]!.element(boundBy: i).frame.size.width * screenshot_image.scale
                                dict["top"] = maindict[type]!.element(boundBy: i).frame.origin.y * screenshot_image.scale
                                dict["left"] = maindict[type]!.element(boundBy: i).frame.origin.x * screenshot_image.scale
                                dict["reference"] = ""
                                dict["text"] = "ios"
                                dict["enabled"] = "true"
                                dict["id"] = ""
                                dict["tempId"] = ""
                                array.append(dict)
                            }
                        }
                        
                    }
                    else if type == "otherElements" || type == "keys"{
                        if label != "" || maindict[type]!.element(boundBy: i).value as! String != "" {
                        let screenshot = XCUIScreen.main.screenshot()
                        let screenshot_image = screenshot.image
                        if label != ""{
                            dict["height"] = maindict[type]!.element(boundBy: i).frame.size.height * screenshot_image.scale
                            dict["width"] = maindict[type]!.element(boundBy: i).frame.size.width  * screenshot_image.scale
                            dict["top"] = maindict[type]!.element(boundBy: i).frame.origin.y * screenshot_image.scale
                            dict["left"] = maindict[type]!.element(boundBy: i).frame.origin.x * screenshot_image.scale
                            dict["reference"] = ""
                            dict["text"] = "ios"
                            dict["enabled"] = "true"
                            dict["id"] = ""
                            dict["tempId"] = ""
                            array.append(dict)
                            continue
                            
                        }
                        else if maindict[type]!.element(boundBy: i).exists{
                            
                            let screenshot = XCUIScreen.main.screenshot()
                            let screenshot_image = screenshot.image
                            dict["height"] = maindict[type]!.element(boundBy: i).frame.size.height * screenshot_image.scale
                            dict["width"] =  maindict[type]!.element(boundBy: i).frame.size.width * screenshot_image.scale
                            dict["top"] =  maindict[type]!.element(boundBy: i).frame.origin.y * screenshot_image.scale
                            dict["left"] =  maindict[type]!.element(boundBy: i).frame.origin.x * screenshot_image.scale
                            dict["reference"] = ""
                            dict["text"] = "ios"
                            dict["enabled"] = "true"
                            dict["id"] = ""
                            dict["tempId"] = ""
                            if label != ""{
                                array.append(dict)
                                continue
                            }
                            else if maindict[type]!.element(boundBy: i).value as! String != "" {
                                dict["tag"] = type
                                dict["custname"] = maindict[type]!.element(boundBy: i).value
                                dict["xpath"] = "bound"+String(i) + "&$#"+type
                                array.append(dict)
                                continue
                            }
                        }
                        else if (maindict[type]![maindict[type]!.element(boundBy: i).identifier]).exists {
                            dict["custname"] = maindict[type]!.element(boundBy: i).identifier
                            dict["xpath"] = maindict[type]!.element(boundBy: i).identifier+"&$#"+type
                            dict["height"] = maindict[type]![maindict[type]!.element(boundBy: i).identifier].frame.size.height * screenshot_image.scale
                            dict["width"] = maindict[type]![maindict[type]!.element(boundBy: i).identifier].frame.size.width  * screenshot_image.scale
                            dict["top"] = maindict[type]![maindict[type]!.element(boundBy: i).identifier].frame.origin.y * screenshot_image.scale
                            dict["left"] = maindict[type]![maindict[type]!.element(boundBy: i).identifier].frame.origin.x * screenshot_image.scale
                            dict["reference"] = ""
                            dict["text"] = "ios"
                            dict["enabled"] = "true"
                            dict["id"] = ""
                            dict["tempId"] = ""
                            if (maindict[type]!.element(boundBy: i).value as! String != ""){
                                array.append(dict)
                                continue
                            }
                            
                        }
                    }
                    }
                    else if label != ""{
                            let screenshot = XCUIScreen.main.screenshot()
                            let screenshot_image = screenshot.image
                            dict["height"] = maindict[type]![maindict[type]!.element(boundBy: i).identifier].firstMatch.frame.size.height * screenshot_image.scale
                            dict["width"] = maindict[type]![maindict[type]!.element(boundBy: i).identifier].firstMatch.frame.size.width  * screenshot_image.scale
                            dict["top"] = maindict[type]![maindict[type]!.element(boundBy: i).identifier].firstMatch.frame.origin.y * screenshot_image.scale
                            dict["left"] = maindict[type]![maindict[type]!.element(boundBy: i).identifier].firstMatch.frame.origin.x * screenshot_image.scale
                            dict["reference"] = ""
                            dict["text"] = "ios"
                            dict["enabled"] = "true"
                            dict["id"] = ""
                            dict["tempId"] = ""
                            array.append(dict)
                            continue
                        
                        }
                        
                    }
                }
                
            }
            
        }
        return array
    
    
    }
}


