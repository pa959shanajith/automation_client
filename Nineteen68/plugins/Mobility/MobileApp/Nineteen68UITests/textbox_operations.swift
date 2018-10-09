//
//  textbox_operations.swift
//  UI Tests
//
//  Created by Nayak Dheeraj on 08/08/18.
//  Copyright © 2018 Nineteen68. All rights reserved.
//

import Foundation
import XCTest

extension XCUIElement {
    /**
     Removes any current text in the field before typing in the new value
     - Parameter text: the text to enter into the field*/
        func clearAndEnterText(_ text: String) -> Void {

        self.tap()

        if let stringValue = self.value as? String {
        let deleteString = stringValue.map { _ in "\u{8}" }.joined(separator: "")
        if deleteString.count > 0 {
        self.typeText(deleteString)
        }
        }

        self.typeText(text)
        }
    }





class type_box_operations{
    
    func type_text(bundle_id:String,querytype:XCUIElementQuery,label:String,input:String)-> String{
        if label.hasPrefix("bound") {
            let str_label = String(label.dropFirst(5))
            let i = Int(str_label)
            if querytype.element(boundBy: i!).exists{
                querytype.element(boundBy: i!).tap()
                querytype.element(boundBy: i!).typeText(input)
                if XCUIApplication(bundleIdentifier: bundle_id).buttons["Done"].exists{
                    XCUIApplication(bundleIdentifier: bundle_id).buttons["Done"].tap()
                }
                return "pass"
            }
            return "fail"
        }
        if querytype[label].exists{
            querytype[label].tap()
            XCUIApplication(bundleIdentifier: bundle_id).typeText(input)
            if XCUIApplication(bundleIdentifier: bundle_id).buttons["Done"].exists{
                XCUIApplication(bundleIdentifier: bundle_id).buttons["Done"].tap()
            }
            return "pass"
        }
        return "fail"
    }
    
    func type_securetext(bundle_id:String,querytype:XCUIElementQuery,label:String,input:String) -> String {
        if label.hasPrefix("bound") {
            let str_label = String(label.dropFirst(5))
            let i = Int(str_label)
            if querytype.element(boundBy: i!).exists{
                querytype.element(boundBy: i!).tap()
                querytype.element(boundBy: i!).typeText(input)
                if XCUIApplication(bundleIdentifier: bundle_id).buttons["Done"].exists{
                    XCUIApplication(bundleIdentifier: bundle_id).buttons["Done"].tap()
                }
                return "pass"
            }
            return "fail"
        }
        if querytype[label].exists{
            querytype[label].tap()
            querytype[label].typeText(input)
            if XCUIApplication(bundleIdentifier: bundle_id).buttons["Done"].exists{
                XCUIApplication(bundleIdentifier: bundle_id).buttons["Done"].tap()
            }
            return "pass"
        }
        return "fail"
        
    }
    
    
    func cleartext(bundle_id:String,querytype:XCUIElementQuery,label:String) -> String{
        if label.hasPrefix("bound") {
            let str_label = String(label.dropFirst(5))
            let i = Int(str_label)
            if querytype.element(boundBy: i!).exists{
                querytype.element(boundBy: i!).clearAndEnterText("")
                return "pass"
            }
            return "fail"
        }
        if querytype[label].exists{
            querytype[label].clearAndEnterText("")
            return "pass"
        }
        return "fail"
        
    }
    
    
    
    func gettext(bundle_id:String,querytype:XCUIElementQuery,label:String)-> String{
        
        if label.hasPrefix("bound") {
            let str_label = String(label.dropFirst(5))
            let i = Int(str_label)
            if querytype.element(boundBy: i!).exists{
                return querytype.element(boundBy: i!).value as! String
            }
            return "fail"
        }
        if querytype[label].exists{
            return querytype[label].value as! String
            
        }
        return "fail"
    }
    
    
        
}

    
  
    
    


        
 
        
       
        /*
        UIPasteboard.general.string = input   // substitute "the password" with the actual password
        querytype[label].doubleTap()      // substitute "PasswordTextField" with appropriate identifier
        app.menuItems["Paste"].tap()
         if label.hasPrefix("bound") {
         let str_label = String(label.dropFirst(5))
         let i = UInt(str_label)
         if querytype.element(boundBy: i!).exists{
         querytype.element(boundBy: i!).tap()
         return "pass"
        */




