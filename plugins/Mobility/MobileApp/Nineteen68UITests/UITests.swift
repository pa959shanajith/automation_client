//
//  UITests.swift
//  UITests
//
//  Created by Nayak Dheeraj
//  Copyright © 2018 Nineteen68. All rights reserved.
//



import UIKit
import XCTest
import SwiftSocket
import Foundation

class UITests: Nineteen68UITests {
    var bundle_id = ""
    var error_msg = ""

    public class UITestObserver: NSObject, XCTestObservation {
        public func testCase(_ testCase: XCTestCase,
                             didFailWithDescription description: String,
                             inFile filePath: String?,
                             atLine lineNumber: Int) {
            print("failure description    : \(description)")
            
            errrorhandle().send_error(message: description)
            
        }
    }
    override func setUp() {
        super.setUp()
        
        //XCUIApplication().launch()
        XCTestObservationCenter.shared.addTestObserver(UITestObserver())
        
    }
    
    
    func testRefreshControl() {
       
        continueAfterFailure = false
        var status = "running"
        //READ IP address of the mobile
        let testBundle = Bundle(for: type(of: self))
        let filePath = testBundle.path(forResource: "data", ofType: "txt")
        XCTAssertNotNil(filePath)
        var read_ip = ""
        do {
            read_ip = try String(contentsOfFile: filePath!, encoding: String.Encoding.utf8)
            
        } catch let error as NSError{
            print("failed to read")
            print(error)
        }
        if Nineteen68UITests.controll_variables.server_status == "down"{
            //start the server
            Nineteen68UITests.controll_variables.server_side = server(ip : read_ip)
            Nineteen68UITests.controll_variables.server_status = "up"
        }
        print("xcode server is running")
        //perform query or execution and return result

        while status=="running"{
            Nineteen68UITests.controll_variables.client = Nineteen68UITests.controll_variables.server_side.accept()
            
            while Nineteen68UITests.controll_variables.client == nil{
                
                Nineteen68UITests.controll_variables.server_side = server(ip : read_ip)
                Nineteen68UITests.controll_variables.client = Nineteen68UITests.controll_variables.server_side.accept()

            }
            
            
            print("Newclient from:\(controll_variables.client?.address)[\(String(describing: controll_variables.client?.port))]")
            let data = Nineteen68UITests.controll_variables.client?.read(5)
            let str = NSString(bytes: data!, length: data!.count, encoding: String.Encoding.utf8.rawValue)
            
            if str == "query"{
                
                let query_status = query_side().query(client: Nineteen68UITests.controll_variables.client!)
                
                
            }
        
            if str == "execu"{
                var result = execution_side().execution(client: Nineteen68UITests.controll_variables.client!)
                errrorhandle().send_screenshot()
                if result[0] == "pass"{
                    let data2 = "pass".data(using: .utf8)
                    Nineteen68UITests.controll_variables.client?.send(data:data2!)
                    Nineteen68UITests.controll_variables.client?.send(string:"terminate")
          
                }
                else if result[0] == "fail"{
                    if Nineteen68UITests.controll_variables.message == ""{
                        let data2 = "fail".data(using: .utf8)
                        Nineteen68UITests.controll_variables.client?.send(data:data2!)
                        Nineteen68UITests.controll_variables.client?.send(string:"terminate")
                    }
                    else {
                        Nineteen68UITests.controll_variables.message = ""
                    }
                }
                else {
                    
                    let passdata = "passval".data(using: .utf8)
                    controll_variables.client?.send(data:passdata!)
                    Nineteen68UITests.controll_variables.client?.send(string:"!@#$%^&*()")
                    let data1 = (result[0]).data(using: .utf8)
                    controll_variables.client?.send(data:data1!)
                    Nineteen68UITests.controll_variables.client?.send(string:"terminate")
                }
            }
            if str == "stop!"{
                status = "stop" 
            }

        }
        
        
    }

}

