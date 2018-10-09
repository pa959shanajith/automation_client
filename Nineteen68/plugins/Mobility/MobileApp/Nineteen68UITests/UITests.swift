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

    func testRefreshControl() {
        continueAfterFailure = true
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
        
        //start the server
        let server_side = server(ip : read_ip)
        print("xcode server is running")
        
        //perform query or execution and return result
        while status=="running"{
            
            let client = server_side.accept()
            print("Newclient from:\(client?.address)[\(String(describing: client?.port))]")
            let data = client?.read(5)
            let str = NSString(bytes: data!, length: data!.count, encoding: String.Encoding.utf8.rawValue)
            
            if str == "query"{
                
                let query_status = query_side().query(client: client!)
                print(query_status)
                
            }
        
            if str == "execu"{
                var result = execution_side().execution(client: client!)
                print(result)
                if result[0] == "pass"{
                    let data2 = "pass".data(using: .utf8)
                    client?.send(data:data2!)
                }
                else if result[0] == "fail"{
                    let data2 = "fail".data(using: .utf8)
                    client?.send(data:data2!)
                }
                else {
                    let passdata = "passval".data(using: .utf8)
                    client?.send(data:passdata!)
                    let data1 = (result[0]).data(using: .utf8)
                    client?.send(data:data1!)
                }
            }
            if str == "stop!"{
                status = "stop" 
            }
        }
        
    }
}

