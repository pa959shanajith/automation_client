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
        
        controll_variables.message = "failure description: " + message
        let data1 = "error".data(using: .utf8)
        controll_variables.client?.send(data:data1!)
        let data2 = controll_variables.message.data(using: .utf8)
        controll_variables.client?.send(data:data2!)
    }
    func redirect(){
        UITests().testRefreshControl()
    }
    
}
