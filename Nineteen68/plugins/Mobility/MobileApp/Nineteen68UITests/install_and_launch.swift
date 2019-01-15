//
//  install_and_launch.swift
//  UI Tests
//
//  Created by Nayak Dheeraj on 08/08/18.
//  Copyright © 2018 Nineteen68. All rights reserved.
//

import Foundation
import XCTest

//launch app with bundle id
//ex-App_Launch(bundle_id: "com.bankofamerica.BofA")
class run_and_kill{
    
    
    
    func App_Launch(bundle_id:String)->String{
        let app=XCUIApplication(bundleIdentifier: bundle_id)
        app.launch()
        return "pass"
    }
    
    func close_application(bundle_id:String)-> String{
        XCUIApplication(bundleIdentifier: bundle_id).terminate()
        return "pass"
    }
    
    //launch app with siri
    //app_name= name of the app
    
    func lauch_siri(app_name:String){
        if #available(iOS 10.3, *) {
            XCUIDevice().siriService.activate(voiceRecognitionText: app_name)
        } else {
            // Fallback on earlier versions
        }
        
    }
    //terminate the activate application
    
    
    func App_Terminate(app:XCUIApplication){
        app.terminate()
        
        
    }
    func sleep_time(time:UInt32){
        sleep(time)
    }
    
    func backpress() -> String{
        XCUIDevice.shared.press(XCUIDevice.Button.home)
        return "pass"

    }
    
}
