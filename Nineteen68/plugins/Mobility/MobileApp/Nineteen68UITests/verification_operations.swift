//
//  verification_operations.swift
//  UI Tests
//
//  Created by Nayak Dheeraj on 30/08/18.
//  Copyright © 2018 Nineteen68. All rights reserved.
//

import Foundation
import XCTest

class verify{
    
    func verify_elementexists(bundle_id:String,label:String,querytype:XCUIElementQuery)->(String){
        
        if label.hasPrefix("bound") {
            let str_label = String(label.dropFirst(5))
            let i = Int(str_label)
            if querytype.element(boundBy: i!).exists{
                return "pass"
            }
            else{
                errrorhandle().send_error(message: "element doesn't exists")
                return "fail"
            }
        }
    
        let element = querytype[label]
        if element.exists{
                return "pass"
        }
            else {
            errrorhandle().send_error(message: "element doesn't exists")
                return "fail"
        }
    }
    func verify_elemendoesnottexists(bundle_id:String,label:String,querytype:XCUIElementQuery)->(String){
        
        if label.hasPrefix("bound") {
            let str_label = String(label.dropFirst(5))
            let i = Int(str_label)
            if querytype.element(boundBy: i!).exists{
                errrorhandle().send_error(message: "element exists")
                return "fail"
            }
            else{
                return "pass"
            }
        }
        
        let element = querytype[label]
        if element.exists{
            errrorhandle().send_error(message: "element exists")
            return "fail"
        }
        else {
            return "pass"
        }
    }
    
    
    func verify_buttonname(label :String,input :String,querytype:XCUIElementQuery) -> (String) {
        
        if label.hasPrefix("bound") {
            let str_label = String(label.dropFirst(5))
            let i = Int(str_label)
            if querytype.element(boundBy: i!).exists{
                
            if querytype.element(boundBy: i!).value as! String == input{
                    return "pass"
                }
            else if querytype.element(boundBy: i!).label == input{
                return "pass"
                }
            else{
                errrorhandle().send_error(message: "element name doesn't match")
                return "fail"
            }
            }
            else{
                errrorhandle().send_error(message: "element doesn't exists")
                return "fail"
            }
            
        }
        if querytype[label].exists{
        
       if querytype[label].value as! String == input{
            return "pass"
        }
        else if( label == input){
                return "pass"
            }
        else{
            errrorhandle().send_error(message: "element name doesn't match")
            return "fail"
            
            }
        }
        else {
            errrorhandle().send_error(message: "element doesn't exists")
            return "fail"
        }
    }
    
    
    func getbuttonname(label:String,querytype:XCUIElementQuery) -> (String) {
        if label.hasPrefix("bound") {
            
            let str_label = String(label.dropFirst(5))
            let i = Int(str_label)
            if querytype.element(boundBy: i!).exists{
            if querytype.element(boundBy: i!).label != ""{
                return querytype.element(boundBy: i!).label
            }
            else{
                return querytype.element(boundBy: i!).value as! String
                }
                
            }
            else{
                errrorhandle().send_error(message: "element doesn't exists")
                return "fail"
            }
        }
        return label
    }
    
    
    func verify_elementenabled(bundle_id:String,label:String,querytype:XCUIElementQuery) -> (String) {
        
        
        if label.hasPrefix("bound") {
            let str_label = String(label.dropFirst(5))
            let i = Int(str_label)
            if querytype.element(boundBy: i!).exists{
            if querytype.element(boundBy: i!).isEnabled{
                return "pass"
            }
            else{
                errrorhandle().send_error(message: "element is disabled")
                return "fail"
            }
            }
            else{
                errrorhandle().send_error(message: "element doesn't exists")
                return "fail"
            }
        }
        let element = querytype[label]
        if element.exists{
        if element.isEnabled{
            return "pass"
        }
        else{
            errrorhandle().send_error(message: "element is disabled")
            return "fail"
            }
        }
        else{
            errrorhandle().send_error(message: "element doesn't exists")
            return "fail"
        }
    
    }
    
    func verify_elementdisabled(bundle_id:String,label:String,querytype:XCUIElementQuery) -> (String) {
        
        
        if label.hasPrefix("bound") {
            let str_label = String(label.dropFirst(5))
            let i = Int(str_label)
            if querytype.element(boundBy: i!).exists{
            if querytype.element(boundBy: i!).isEnabled{
                errrorhandle().send_error(message: "element is enabled")
                return "fail"
            }
            else{
                return "pass"
            }
                
            }
            else{
                errrorhandle().send_error(message: "element doesn't exists")
                return "fail"
            }
        }
        let element = querytype[label]
        if element.exists == false{
            errrorhandle().send_error(message: "element doesn't exists")
            return "fail"
        }
        if element.isEnabled{
            errrorhandle().send_error(message: "element is enabled")
            return "fail"
        }
        else{
            return "pass"
        }
        
    }
    
    
    func verify_visible(bundle_id:String,label:String,querytype:XCUIElementQuery) -> (String) {
        
        if label.hasPrefix("bound") {
            let str_label = String(label.dropFirst(5))
            let i = Int(str_label)
            if querytype.element(boundBy: i!).exists == false{
                errrorhandle().send_error(message: "element doesn't exists")
                return "fail"
            }
            if querytype.element(boundBy: i!).isHittable{
                var maxY = XCUIApplication(bundleIdentifier: bundle_id).otherElements.element(boundBy: 0).frame.maxY
                if (XCUIApplication(bundleIdentifier: bundle_id).frame.maxY >= maxY)
                {
                   maxY =  XCUIApplication(bundleIdentifier: bundle_id).frame.maxY
                }
                if querytype.element(boundBy: i!).frame.minY < maxY{
                     if querytype.element(boundBy: i!).frame.minY < 1{
                        errrorhandle().send_error(message: "element is not visible on screen")
                        return "fail"
                    }
                    return "pass"
                }
                else{
                    errrorhandle().send_error(message: "element is not visible on screen")
                    return "fail"
                }
            }
            else{
                errrorhandle().send_error(message: "element is not visible on screen and not hittable")
                return "fail"
            }
        }
        let element = querytype[label]
        if element.exists == false{
            errrorhandle().send_error(message: "element is doesn't exists")
            return "fail"
        }
        if element.isHittable{
            print(XCUIApplication(bundleIdentifier: bundle_id).otherElements.element(boundBy: 0).frame.maxY)
            print(element.frame.minY)
            var maxY = XCUIApplication(bundleIdentifier: bundle_id).otherElements.element(boundBy: 0).frame.maxY
            if (XCUIApplication(bundleIdentifier: bundle_id).frame.maxY >= maxY)
            {
                maxY =  XCUIApplication(bundleIdentifier: bundle_id).frame.maxY
            }
            if element.frame.minY < maxY{
                if element.frame.minY < 1{
                    errrorhandle().send_error(message: "element is not visible on screen")
                    return "fail"
                }
                return "pass"
            }
            else{
                errrorhandle().send_error(message: "element is not visible on screen")
                return "fail"
            }
        }
        else{
            errrorhandle().send_error(message: "element is not visible on screen and not hittable")
            return "fail"
        }
        
    }

    func verify_hidden(bundle_id:String,label:String,querytype:XCUIElementQuery) -> (String) {
        if label.hasPrefix("bound") {
            let str_label = String(label.dropFirst(5))
            let i = Int(str_label)
            if querytype.element(boundBy: i!).exists == false{
                errrorhandle().send_error(message: "element is doesn't exists")
                return "fail"
            }
            if querytype.element(boundBy: i!).isHittable{
                var maxY = XCUIApplication(bundleIdentifier: bundle_id).otherElements.element(boundBy: 0).frame.maxY
                if (XCUIApplication(bundleIdentifier: bundle_id).frame.maxY >= maxY)
                {
                    maxY =  XCUIApplication(bundleIdentifier: bundle_id).frame.maxY
                }
                if querytype.element(boundBy: i!).frame.minY < maxY{
                    if querytype.element(boundBy: i!).frame.minY < 1{
                        return "pass"
                        
                    }
                    errrorhandle().send_error(message: "element is visible on screen")
                    return "fail"
                }
                else{
                    return "pass"
                }
            }
            else{
                return "pass"
            }
        }
        let element = querytype[label]
        if element.exists == false{
            errrorhandle().send_error(message: "element is doesn't exists")
            return "fail"
        }
        if element.isHittable{
            var maxY = XCUIApplication(bundleIdentifier: bundle_id).otherElements.element(boundBy: 0).frame.maxY
            if (XCUIApplication(bundleIdentifier: bundle_id).frame.maxY >= maxY)
            {
                maxY =  XCUIApplication(bundleIdentifier: bundle_id).frame.maxY
            }
            if element.frame.minY < maxY{
                if element.frame.minY < 1{
                    return "pass"
                }
                errrorhandle().send_error(message: "element is visible on screen")
                return "fail"
            }
            else{
                return "pass"
            }
        }
        else{
            return "pass"
        }
        
      
    }
 
    func wait_for_elementexists(bundle_id:String,label:String,querytype:XCUIElementQuery) -> (String){
        var sleep_time = 0
        if label.hasPrefix("bound") {
            let str_label = String(label.dropFirst(5))
            let i = Int(str_label)
            
            while querytype.element(boundBy: i!).exists == false{
                sleep(1)
                sleep_time = sleep_time + 1
                if sleep_time == 20 {
                    errrorhandle().send_error(message: "waited for 20 sec element doesn't exists")
                    return "fail"
                }
            }
            if querytype.element(boundBy: i!).exists{
                return "pass"
            }else{
                errrorhandle().send_error(message: "element doesn't exists")
                return "fail"
            }
        }
        let element = querytype[label]
        while element.exists == false {
            sleep(1)
            sleep_time = sleep_time + 1
            if sleep_time == 20 {
                errrorhandle().send_error(message: "waited for 20 sec element doesn't exists")
                return "fail"
            }
        }
        if element.exists{
            return "pass"
        }
        else{
            errrorhandle().send_error(message: "element doesn't exists")
            return "fail"
        }
    }
    func verify_text(bundle_id:String,label:String,querytype:XCUIElementQuery,input:String) -> (String){
        if label.hasPrefix("bound") {
            let str_label = String(label.dropFirst(5))
            let i = Int(str_label)
            if querytype.element(boundBy: i!).exists == false{
                errrorhandle().send_error(message: "element is doesn't exists")
                return "fail"
            }
            if querytype.element(boundBy: i!).value as! String == input{
                return "pass"
            }
            else{
                errrorhandle().send_error(message: "text doesn't match")
                return "fail"
            }
            
        }
        if querytype[label].exists == false{
            errrorhandle().send_error(message: "element is doesn't exists")
            return "fail"
        }

        if querytype[label].value as! String == input{
            return "pass"
        }
        else{
            errrorhandle().send_error(message: "text doesn't match")
            return "fail"}
    }
    


}
