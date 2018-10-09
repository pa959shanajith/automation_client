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
                return "fail"
            }
        }
    
        let element = querytype[label]
        if element.exists{
                return "pass"
        }
            else {
                return "fail"
        }
    }
    func verify_elemendoesnottexists(bundle_id:String,label:String,querytype:XCUIElementQuery)->(String){
        
        if label.hasPrefix("bound") {
            let str_label = String(label.dropFirst(5))
            let i = Int(str_label)
            if querytype.element(boundBy: i!).exists{
                return "fail"
            }
            else{
                return "pass"
            }
        }
        
        let element = querytype[label]
        if element.exists{
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
            if querytype.element(boundBy: i!).label == input{
                return "pass"
                }
            else if querytype.element(boundBy: i!).value as! String == input{
                    return "pass"
                }
            else{
                return "fail"
            }
            
        }
        if( label == input){
            return "pass"
        }
        else{
            return "fail"}
    }
    
    
    func getbuttonname(label:String,querytype:XCUIElementQuery) -> (String) {
        if label.hasPrefix("bound") {
            
            let str_label = String(label.dropFirst(5))
            let i = Int(str_label)
            if querytype.element(boundBy: i!).label != ""{
                return querytype.element(boundBy: i!).label
            }
            else{
                return querytype.element(boundBy: i!).value as! String
            }
        }
        return label
    }
    
    
    func verify_elementenabled(bundle_id:String,label:String,querytype:XCUIElementQuery) -> (String) {
        
        
        if label.hasPrefix("bound") {
            let str_label = String(label.dropFirst(5))
            let i = Int(str_label)
            if querytype.element(boundBy: i!).isEnabled{
                return "pass"
            }
            else{
                return "fail"
            }
        }
        let element = querytype[label]
        if element.isEnabled{
            return "pass"
        }
        else{
            return "fail"
        }
    
    }
    
    func verify_elementdisabled(bundle_id:String,label:String,querytype:XCUIElementQuery) -> (String) {
        
        
        if label.hasPrefix("bound") {
            let str_label = String(label.dropFirst(5))
            let i = Int(str_label)
            if querytype.element(boundBy: i!).isEnabled{
                return "fail"
            }
            else{
                return "pass"
            }
        }
        let element = querytype[label]
        if element.isEnabled{
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
            if querytype.element(boundBy: i!).isHittable{
                let maxY = XCUIApplication(bundleIdentifier: bundle_id).otherElements.element(boundBy: 0).frame.maxY
                print(maxY)
                print(querytype.element(boundBy: i!).frame.minY < maxY)
                if querytype.element(boundBy: i!).frame.minY < maxY{
                     if querytype.element(boundBy: i!).frame.minY < 1{
                        return "fail"
                    }
                    return "pass"
                }
                else{
                    return "fail"
                }
            }
            else{
                return "fail"
            }
        }
        let element = querytype[label]
        if element.isHittable{
            print(XCUIApplication(bundleIdentifier: bundle_id).otherElements.element(boundBy: 0).frame.maxY)
            print(element.frame.minY)
            let maxY = XCUIApplication(bundleIdentifier: bundle_id).otherElements.element(boundBy: 0).frame.maxY
            if element.frame.minY < maxY{
                if element.frame.minY < 1{
                    return "fail"
                }
                return "pass"
            }
            else{
                return "fail"
            }
        }
        else{
            return "fail"
        }
        
    }

    func verify_hidden(bundle_id:String,label:String,querytype:XCUIElementQuery) -> (String) {
        if label.hasPrefix("bound") {
            let str_label = String(label.dropFirst(5))
            let i = Int(str_label)
            if querytype.element(boundBy: i!).isHittable{
                let maxY = XCUIApplication(bundleIdentifier: bundle_id).otherElements.element(boundBy: 0).frame.maxY
                if querytype.element(boundBy: i!).frame.minY < maxY{
                    if querytype.element(boundBy: i!).frame.minY < 1{
                        return "pass"
                        
                    }
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
        if element.isHittable{
            print(XCUIApplication(bundleIdentifier: bundle_id).otherElements.element(boundBy: 0).frame.maxY)
            print(element.frame.minY)
            let maxY = XCUIApplication(bundleIdentifier: bundle_id).otherElements.element(boundBy: 0).frame.maxY
            if element.frame.minY < maxY{
                if element.frame.minY < 1{
                    return "pass"
                }
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
        
        if label.hasPrefix("bound") {
            let str_label = String(label.dropFirst(5))
            let i = Int(str_label)
            
            while querytype.element(boundBy: i!).exists == false{
                sleep(1)
            }
            if querytype.element(boundBy: i!).exists{
                return "pass"
            }
            else{
                return "fail"
            }
        }
        let element = querytype[label]
        while element.exists == false {
            sleep(1)
        }
        if element.exists{
            return "pass"
        }
        else{
            return "fail"
        }
    }
    func verify_text(bundle_id:String,label:String,querytype:XCUIElementQuery,input:String) -> (String){
        if label.hasPrefix("bound") {
            let str_label = String(label.dropFirst(5))
            let i = Int(str_label)
            if querytype.element(boundBy: i!).value as! String == input{
                return "pass"
            }
            else{
                return "fail"
            }
            
        }
        if querytype[label].value as! String == input{
            return "pass"
        }
        else{
            return "fail"}
    }
    


}
