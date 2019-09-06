//
//  query_side.swift
//  UI Tests
//
//  Created by Nayak Dheeraj on 10/08/18.
//  Copyright © 2018 Nineteen68. All rights reserved.
//



import XCTest
import Foundation
import SwiftSocket
import SwiftyJSON
import UIKit


class query_side{
    func JSONStringify(value: AnyObject,prettyPrinted:Bool = false) -> String{
        
        let options = prettyPrinted ? JSONSerialization.WritingOptions.prettyPrinted : JSONSerialization.WritingOptions(rawValue: 0)
        
        
        if JSONSerialization.isValidJSONObject(value) {
            
            do{
                let data = try JSONSerialization.data(withJSONObject: value, options: options)
                if let string = NSString(data: data, encoding: String.Encoding.utf8.rawValue) {
                    return string as String
                }
            }catch {
                
                print("error")
                //Access error here
            }
            
        }
        return ""
        
    }
    func query(client : TCPClient) -> (String) {
        
        
        
        var data = client.read(2)
        let strnum = NSString(bytes: data!, length: data!.count, encoding: String.Encoding.utf8.rawValue)
        let num=strnum!
        let exampeStruct = Int(num.intValue)
        data = client.read(exampeStruct)
        let str = NSString(bytes: data!, length: data!.count, encoding: String.Encoding.utf8.rawValue)
        let bundleId = str! as String
        print(bundleId)
        
        let dict = xcelement_query().dispatch(bundle_id:bundleId , querytype: ["otherElements","Button","XCUIElementTypeSecureTextField","XCUIElementTypeSearchField","RadioButton","CheckBox","statictexts","links","cells","image","keys","datePickers","switches","XCUIElementTypeSlider","activityIndicators","progressIndicators","EditText","textViews","XCUIElementTypePickerWheel"])
        
        //var jsonObj = JSON(dict)
        //let string = jsonObj.rawString()
        
        let jsonString = JSONStringify(value: dict as AnyObject)
        var str_data = jsonString.data(using: .utf8)
        client.send(data:str_data!)
        client.send(string:"!@#$%^&*()")
        
        
        
        

        //send current screenshot in base64
        let screenshot = XCUIScreen.main.screenshot()
        let screenshot_image = screenshot.image
        let screenshot_png = UIImagePNGRepresentation(screenshot_image)
        let img_data = screenshot_png?.base64EncodedString(options: .lineLength64Characters)
        //img_data = img_data! + "!@#$%^&*()"
        client.send(string : img_data!)
        client.send(string:"!@#$%^&*()" )
        
        
        
        
        
        //send height
        let heightInPoints = screenshot_image.size.height
        let heightInPixels = heightInPoints * screenshot_image.scale
        let heightInPixels_str = String(format: "%.3f", Double(heightInPixels))
        str_data = heightInPixels_str.data(using: .utf8)
        client.send(data: str_data!)
        client.send(string:"!@#$%^&*()")
        
        
        //send width
        let widthInPoints = screenshot_image.size.width
        let widthInPixels = widthInPoints * screenshot_image.scale
        let widthInPixels_str = String(format: "%.3f", Double(widthInPixels))
        str_data = widthInPixels_str.data(using: .utf8)
        client.send(data: str_data!)
        client.send(string:"final")
        
        
        
        
    
    return "scrape complete"
    }
    
    
}

