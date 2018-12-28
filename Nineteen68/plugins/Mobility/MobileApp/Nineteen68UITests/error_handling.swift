//
//  error_handling.swift
//  UI Tests
//
//  Created by Nayak Dheeraj on 08/08/18.
//  Copyright © 2018 Nineteen68. All rights reserved.
//

import Foundation
import SwiftSocket
import XCTest
import SwiftyJSON


class errrorhandle: UITests {
    
    func send_error(message:String){
        send_screenshot()
        controll_variables.message = "failure description: " + message
        let data1 = "error".data(using: .utf8)
        controll_variables.client?.send(data:data1!)
        controll_variables.client?.send(string:"!@#$%^&*()")
        let data2 = controll_variables.message.data(using: .utf8)
        controll_variables.client?.send(data:data2!)
        controll_variables.client?.send(string : "terminate")
    }
    func redirect(){
        UITests().testRefreshControl()
    }
    func send_screenshot(){
        //send current screenshot in base64
        let screenshot = XCUIScreen.main.screenshot()
        let screenshot_image = screenshot.image
        let screenshot_png = UIImagePNGRepresentation(screenshot_image)
        let img_data = screenshot_png?.base64EncodedString(options: .lineLength64Characters)
        //img_data = img_data! + "!@#$%^&*()"
        controll_variables.client?.send(string : img_data!)
        controll_variables.client?.send(string : "!@#$%^&*()")
        
    }
    
}
