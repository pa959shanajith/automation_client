//
//  Nineteen68UITests.swift
//  Nineteen68UITests
//
//  Created by Nayak Dheeraj on 06/09/18.
//  Copyright © 2018 Nineteen68. All rights reserved.
//

import XCTest
import SwiftSocket

class Nineteen68UITests: XCTestCase {
    let app = XCUIApplication()
    
    struct controll_variables {
        static var message = ""
        static var client = TCPServer(address: "", port: 8022).accept()
        static var server_side = TCPServer(address: "", port: 8022)
        static var server_status = "down"
        static var server = TCPServer(address: "", port: 8022)

    }
    
    func XCTAbortTest(_ message: String,
                      file: StaticString = #file, line: UInt = #line
        ) -> Never {
        self.continueAfterFailure = false
        XCTFail(message, file: file, line: line)
        fatalError("never reached")
        
        
    }
    
    override func setUp() {
        super.setUp()
        continueAfterFailure = false

    }



    override func tearDown() {
        super.tearDown()
         errrorhandle().redirect()
        
            //app.terminate()
    }

    
  
    func waitForElementToAppear(_ element: XCUIElement, file: String = #file, line: UInt = #line) {
        let existsPredicate = NSPredicate(format: "exists == true")
        expectation(for: existsPredicate, evaluatedWith: element, handler: nil)
        
        waitForExpectations(timeout: 1) { (error) -> Void in
            if (error != nil) {
                let message = "Failed to find \(element) after 5 seconds."
                self.recordFailure(withDescription: message, inFile: file, atLine: Int(line), expected: true)
                self.continueAfterFailure = true//edit
                
            }

        }
    }
    
}


