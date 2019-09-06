//
//  performing_guesture.swift
//  UI Tests
//
//  Created by Nayak Dheeraj on 08/08/18.
//  Copyright © 2018 Nineteen68. All rights reserved.
//

import Foundation

import Foundation
import XCTest
extension XCUIElement
{
    enum direction : Int {
        case Up, Down, Left, Right
    }
    
    func gentleSwipe(_ direction : direction) {
        let half : CGFloat = 0.5/2
        let adjustment : CGFloat = 0.25/2
        let pressDuration : TimeInterval = 0.05/2
        
        let lessThanHalf = half - adjustment
        let moreThanHalf = half + adjustment
        
        let centre = self.coordinate(withNormalizedOffset: CGVector(dx: half, dy: half))
        let aboveCentre = self.coordinate(withNormalizedOffset: CGVector(dx: half, dy: lessThanHalf))
        let belowCentre = self.coordinate(withNormalizedOffset: CGVector(dx: half, dy: moreThanHalf))
        let leftOfCentre = self.coordinate(withNormalizedOffset: CGVector(dx: lessThanHalf, dy: half))
        let rightOfCentre = self.coordinate(withNormalizedOffset: CGVector(dx: moreThanHalf, dy: half))
        
        switch direction {
        case .Up:
            centre.press(forDuration: pressDuration, thenDragTo: aboveCentre)
            break
        case .Down:
            centre.press(forDuration: pressDuration, thenDragTo: belowCentre)
            break
        case .Left:
            centre.press(forDuration: pressDuration, thenDragTo: leftOfCentre)
            break
        case .Right:
            centre.press(forDuration: pressDuration, thenDragTo: rightOfCentre)
            break
        }
    }
}

class performing_guestures{
    

    func tap(querytype:XCUIElementQuery,label:String)-> String{
        

        
        if label.hasPrefix("bound") {
           let str_label = String(label.dropFirst(5))
           let i = Int(str_label)
            if querytype.element(boundBy: i!).exists{
                querytype.element(boundBy: i!).tap()
                return "pass"
            }
            errrorhandle().send_error(message: "tap action failed element doesn't exist")
            return "fail"
        }
        else{
            let element = querytype[label]
            if element.exists{
                 element.tap()
                return "pass"
            }
            errrorhandle().send_error(message: "tap action failed element doesn't exist")
            return "fail"
        }

    }
    
    
    func long_press(querytype:XCUIElementQuery,label:String,forDuration:TimeInterval)-> String{
        let element = querytype[label]
        if label.hasPrefix("bound") {
            let str_label = String(label.dropFirst(5))
            let i = Int(str_label)
            if querytype.element(boundBy: i!).exists{
                querytype.element(boundBy: i!).press(forDuration: forDuration)
                return "pass"
            }
            errrorhandle().send_error(message: "longpress failed element doesn't exist")
            return "fail"
        }
        else{
            if element.exists{
                element.press(forDuration: forDuration)
                return "pass"
            }
            errrorhandle().send_error(message: "longpress element doesn't exist")
            return "fail"
        }
  
    }
    
    // set_to -> between 0 to 1
    func adjusting_Slider(querytype:XCUIElementQuery,label:String,set_to:CGFloat) -> String {
        if set_to > 1 {
            errrorhandle().send_error(message: "adjusting slider input should lie in between 0 and 1")
            return "fail"
        }
        let element = querytype[label]
        if label.hasPrefix("bound") {
            let str_label = String(label.dropFirst(5))
            let i = Int(str_label)
            if querytype.element(boundBy: i!).exists{
                var input_val = querytype.element(boundBy: i!).value as! String
                var num:Double = 0.0
                if input_val.hasSuffix("%"){
                    input_val = String(input_val.dropLast())
                    num = Double(input_val)!/100
                }
                let slider = querytype.element(boundBy: i!)
                var old_val = slider.coordinate(withNormalizedOffset: CGVector(dx: num, dy: 0.5))
                let new_val = slider.coordinate(withNormalizedOffset: CGVector(dx: set_to, dy: 0.5))
                old_val.press(forDuration: 0.1, thenDragTo: new_val)
                //querytype.element(boundBy: i!).adjust(toNormalizedSliderPosition: set_to)
                return "pass"
            }
            errrorhandle().send_error(message: "adjusting slider action failed element doesn't exist")
            return "fail"
        }
        else{
            if element.exists{
                var input_val = element.value as! String
                var num:Double = 0.0
                if input_val.hasSuffix("%"){
                    input_val = String(input_val.dropLast())
                    num = Double(input_val)!/100
                }
                var old_val = element.coordinate(withNormalizedOffset: CGVector(dx: num, dy: 0.5))
                let new_val = element.coordinate(withNormalizedOffset: CGVector(dx: set_to, dy: 0.5))
                old_val.press(forDuration: 0.1, thenDragTo: new_val)
                //element.adjust(toNormalizedSliderPosition: set_to)
                return "pass"

            }
            errrorhandle().send_error(message: "adjusting slider action failed element doesn't exist")
            return "fail"
        }
       
    }

    
    
    func doubletap(querytype:XCUIElementQuery,label:String)-> String{
        if label.hasPrefix("bound") {
            let str_label = String(label.dropFirst(5))
            let i = Int(str_label)
            if querytype.element(boundBy: i!).exists{
                querytype.element(boundBy: i!).doubleTap()
                return "pass"
            }
            errrorhandle().send_error(message: "element doesn't exist")
            return "fail"
        }
        else{
            let element = querytype[label]
            if element.exists{
                element.doubleTap()
                return "pass"
            }
            errrorhandle().send_error(message: "element doesn't exist")
            return "fail"
        }
        
    }
    
    
    func swipe_up(querytype:XCUIElementQuery,label:String)-> String{
        if (label == "empty") {
            XCUIApplication(bundleIdentifier: bundle_id).swipeUp()
            return "pass"
        }
        if label.hasPrefix("bound") {
            let str_label = String(label.dropFirst(5))
            let i = Int(str_label)
            if querytype.element(boundBy: i!).exists{
                querytype.element(boundBy: i!).swipeUp()
                return "pass"
            }
            errrorhandle().send_error(message: "element doesn't exist")
            return "fail"
        }
        else{
            let element = querytype[label]
            if element.exists{
                element.swipeUp()
                return "pass"
            }
            errrorhandle().send_error(message: "element doesn't exist")
            return "fail"
        }
    }
    
    
    
    
    func swipe_down(querytype:XCUIElementQuery,label:String)-> String{
        if (label == "empty") {
            XCUIApplication(bundleIdentifier: bundle_id).swipeDown()
            return "pass"
        }
        if label.hasPrefix("bound") {
            let str_label = String(label.dropFirst(5))
            let i = Int(str_label)
            if querytype.element(boundBy: i!).exists{
                querytype.element(boundBy: i!).swipeDown()
                return "pass"
            }
            errrorhandle().send_error(message: "element doesn't exist")
            return "fail"
        }
        else{
            let element = querytype[label]
            if element.exists{
                element.swipeDown()
                return "pass"
            }
            errrorhandle().send_error(message: "element doesn't exist")
            return "fail"
        }
    }
    
    
    
    func swipe_right(querytype:XCUIElementQuery,label:String)-> String{
        if (label == "empty") {
            XCUIApplication(bundleIdentifier: bundle_id).swipeRight()
            return "pass"
        }
        if label.hasPrefix("bound") {
            let str_label = String(label.dropFirst(5))
            let i = Int(str_label)
            if querytype.element(boundBy: i!).exists{
                querytype.element(boundBy: i!).swipeRight()
                return "pass"
            }
            errrorhandle().send_error(message: "element doesn't exist")
            return "fail"
        }
        else{
            let element = querytype[label]
            if element.exists{
                element.swipeRight()
                return "pass"
            }
            errrorhandle().send_error(message: "element doesn't exist")
            return "fail"
        }
        
    }
    
    
    
    
    func swipe_left(querytype:XCUIElementQuery,label:String)-> String {
        if (label == "empty") {
            XCUIApplication(bundleIdentifier: bundle_id).swipeLeft()
            return "pass"
        }
        if label.hasPrefix("bound") {
            let str_label = String(label.dropFirst(5))
            let i = Int(str_label)
            if querytype.element(boundBy: i!).exists{
                querytype.element(boundBy: i!).swipeLeft()
                return "pass"
            }
            errrorhandle().send_error(message: "element doesn't exist")
            return "fail"
        }
        else{
            let element = querytype[label]
            if element.exists{
                element.swipeLeft()
                return "pass"
            }
            errrorhandle().send_error(message: "element doesn't exist")
            return "fail"
        }
  
    }
    
    func select_radio_checkbox(querytype:XCUIElementQuery,label:String)-> String {
        if label.hasPrefix("bound") {
            let str_label = String(label.dropFirst(5))
            let i = Int(str_label)
            if querytype.element(boundBy: i!).exists{
                if querytype.element(boundBy: i!).isSelected{
                    return "pass"
                }
                else{
                    querytype.element(boundBy: i!).tap()
                    return "pass"
                    
                    }
                }
            else{
                errrorhandle().send_error(message: "element doesn't exist")
                return "fail"
            }
        
        }
        else{
            let element = querytype[label]
            if element.exists{
                if element.isSelected{
                    return "pass"
                }
                else{
                    element.tap()
                    return "pass"
                }
            }
            else{
                errrorhandle().send_error(message: "element doesn't exist")
                return "fail"
            }
    }
    }
    
    func unselect_checkbox(querytype:XCUIElementQuery,label:String) -> String{
        if label.hasPrefix("bound") {
            let str_label = String(label.dropFirst(5))
            let i = Int(str_label)
            if querytype.element(boundBy: i!).exists{
                if querytype.element(boundBy: i!).isSelected{
                    querytype.element(boundBy: i!).tap()
                    return "pass"
                }
                else{
                    return "pass"
                    
                }
            }
            else{
                errrorhandle().send_error(message: "element doesn't exist")
                return "fail"
            }
            
        }
        else{
            let element = querytype[label]
            if element.exists{
                if element.isSelected{
                    element.tap()
                    return "pass"
                }
                else{
                    
                    return "pass"
                }
            }
            else{
                errrorhandle().send_error(message: "element doesn't exist")
                return "fail"
            }
        }
   
    }
    
 
    func get_status(querytype:XCUIElementQuery,label:String) -> String{
        if label.hasPrefix("bound") {
            let str_label = String(label.dropFirst(5))
            let i = Int(str_label)
            if querytype.element(boundBy: i!).exists{
                if querytype.element(boundBy: i!).value as! String != ""{
                    return querytype.element(boundBy: i!).value as! String
                }
                else{
                    
                    return querytype.element(boundBy: i!).label
                    
                }
            }
            else{
                errrorhandle().send_error(message: "element doesn't exist")
                return "fail"
            }
            
        }
        else{
            let element = querytype[label]
            if element.exists{
                if element.value as! String != ""{
                    return element.value as! String
                }
                else{
                    
                    return element.label
                }
            }
            else{
                errrorhandle().send_error(message: "element doesn't exist")
                return "fail"
            }
        }
    }
   
    
    //Initiates a press-and-hold gesture, then drags to another element. send two label and query type
    func press_drag(querytype:XCUIElementQuery,label:   String,forDuration:TimeInterval,thenDragTo:XCUIElementQuery,label2:String){
        let element = querytype[label]
        let thenDragTo = thenDragTo[label2]
        
        if element.exists{
            return element.press(forDuration: forDuration,thenDragTo: thenDragTo)
        }else {
            errrorhandle().send_error(message: "element doesn't exist")
            print("element does not exists")
        }
    }
    
    func set_value(querytype:XCUIElementQuery,label:String,input :String) -> String {
        if label.hasPrefix("bound") {
            
            let str_label = String(label.dropFirst(5))
            let i = Int(str_label)
            
            if querytype.element(boundBy: i!).exists{
                querytype.element(boundBy: i!).adjust(toPickerWheelValue: input)
            return "pass"
                
            }
            else{
                errrorhandle().send_error(message: "element doesn't exist")
                return "fail"
            }
            
        }
        else{
            
            let element = querytype[label]
            if element.exists{
                element.adjust(toPickerWheelValue: input)
                return "pass"

            }
            else {
                errrorhandle().send_error(message: "element doesn't exist")
                return "fail"
            }
        }
    }
    func get_value(querytype:XCUIElementQuery,label:String) -> String {
        if label.hasPrefix("bound") {
            let str_label = String(label.dropFirst(5))
            let i = Int(str_label)
            if querytype.element(boundBy: i!).exists{
                
                let value = querytype.element(boundBy: i!).value
                return value as! String
                
            }
            else{
                errrorhandle().send_error(message: "element doesn't exist")
                return "fail"
            }
            
        }
        else{
            
            let element = querytype[label]
            if element.exists{
                let value = element.value
                return value as! String
                
            }
            else {
                errrorhandle().send_error(message: "element doesn't exist")
                return "fail"
            }
        }
    }
    func tap_with_cordinates(bundleid :String ){
        let app = XCUIApplication(bundleIdentifier: bundleid)
        let normalized = app.coordinate(withNormalizedOffset: CGVector(dx: 0, dy: 0))
        let coordinate = normalized.withOffset(CGVector(dx: 500, dy: 1200))
        coordinate.doubleTap()
        
    }
    
    }


