//
//  Nineteen68UITests.swift
//  Nineteen68UITests
//
//  Created by Nayak Dheeraj on 06/09/18.
//  Copyright © 2018 Nineteen68. All rights reserved.
//

import XCTest

class Nineteen68UITests: XCTestCase {
    let app = XCUIApplication()
    
    override func setUp() {
        super.setUp()
        continueAfterFailure = true
        app.launch()
    }
    

    override func tearDown() {
        super.tearDown()
        app.terminate()
    }
    
    
    
    func waitForElementToAppear(_ element: XCUIElement, file: String = #file, line: UInt = #line) {
        let existsPredicate = NSPredicate(format: "exists == true")
        expectation(for: existsPredicate, evaluatedWith: element, handler: nil)
        
        waitForExpectations(timeout: 5) { (error) -> Void in
            if (error != nil) {
                let message = "Failed to find \(element) after 5 seconds."
                self.recordFailure(withDescription: message, inFile: file, atLine: Int(line), expected: true)
            }
        }
    }
}

