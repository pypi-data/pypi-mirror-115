if __name__ == '__main__':

  import sys
  import os
  dir_path = os.path.dirname(os.path.realpath(__file__))

  from zebrazoom.code.vars import getGlobalVariables
  globalVariables = getGlobalVariables()

  if len(sys.argv) == 1:
    
    print("The data produced by ZebraZoom can be found in the folder: " + os.path.join(dir_path,'ZZoutput'))
    from zebrazoom.GUIAllPy import SampleApp
    app = SampleApp()
    app.mainloop()
      
  else:

    if sys.argv[1] == "getTailExtremityFirstFrame":
      
      pathToVideo = sys.argv[2]
      videoName   = sys.argv[3]
      videoExt    = sys.argv[4]
      configFile  = sys.argv[5]
      argv        = sys.argv
      argv.pop(0)
      from zebrazoom.getTailExtremityFirstFrame import getTailExtremityFirstFrame
      __spec__ = "ModuleSpec(name='builtins', loader=<class '_frozen_importlib.BuiltinImporter'>)"
      getTailExtremityFirstFrame(pathToVideo, videoName, videoExt, configFile, argv)
        
    elif sys.argv[1] == "recreateSuperStruct":
      
      pathToVideo = sys.argv[2]
      videoName   = sys.argv[3]
      videoExt    = sys.argv[4]
      configFile  = sys.argv[5]
      argv        = sys.argv
      argv.pop(0)
      from zebrazoom.recreateSuperStruct import recreateSuperStruct
      __spec__ = "ModuleSpec(name='builtins', loader=<class '_frozen_importlib.BuiltinImporter'>)"
      recreateSuperStruct(pathToVideo, videoName, videoExt, configFile, argv)
        
    elif sys.argv[1] == "convertSeqToAvi":
      
      from zebrazoom.videoFormatConversion.seq_to_avi import sqb_convert_to_avi
      path      = sys.argv[2]
      videoName = sys.argv[3]
      if len(sys.argv) == 5:
        lastFrame = int(sys.argv[4])
      else:
        lastFrame = -1
      sqb_convert_to_avi(path, videoName, lastFrame)

    elif sys.argv[1] == "dataPostProcessing":
      
      if sys.argv[2] == "sleepVsMoving":
        from zebrazoom.code.dataPostProcessing.findSleepVsMoving import calculateSleepVsMovingPeriods
        pathToZZoutput = os.path.join(dir_path,'ZZoutput')
        videoName      = sys.argv[3]
        speedThresholdForMoving = float(sys.argv[4])
        notMovingNumberOfFramesThresholdForSleep = int(sys.argv[5])
        if len(sys.argv) >= 7:
         specifiedStartTime  = sys.argv[6]
        else:
          specifiedStartTime = 0
        if len(sys.argv) >= 8:
          distanceTravelledRollingMedianFilter = int(sys.argv[7])
        else:
          distanceTravelledRollingMedianFilter = 0
        if len(sys.argv) >= 10:
          videoPixelSize = float(sys.argv[8])
          videoFPS = float(sys.argv[9])
        else:
          videoPixelSize = -1
          videoFPS = -1
        calculateSleepVsMovingPeriods(pathToZZoutput, videoName, speedThresholdForMoving, notMovingNumberOfFramesThresholdForSleep, specifiedStartTime, distanceTravelledRollingMedianFilter, videoPixelSize, videoFPS)
      
      if sys.argv[2] == "firstSleepingTimeAfterSpecifiedTime":
        from zebrazoom.code.dataPostProcessing.findSleepVsMoving import firstSleepingTimeAfterSpecifiedTime
        pathToZZoutput = os.path.join(dir_path,'ZZoutput')
        videoName      = sys.argv[3]
        specifiedTime  = sys.argv[4]
        wellNumber     = sys.argv[5]
        firstSleepingTimeAfterSpecifiedTime(pathToZZoutput, videoName, specifiedTime, wellNumber)
      
      if sys.argv[2] == "numberOfSleepingAndMovingTimesInTimeRange":
        from zebrazoom.code.dataPostProcessing.findSleepVsMoving import numberOfSleepingAndMovingTimesInTimeRange
        pathToZZoutput     = os.path.join(dir_path,'ZZoutput')
        videoName          = sys.argv[3]
        specifiedStartTime = sys.argv[4]
        specifiedEndTime   = sys.argv[5]
        wellNumber         = sys.argv[6]
        numberOfSleepingAndMovingTimesInTimeRange(pathToZZoutput, videoName, specifiedStartTime, specifiedEndTime, wellNumber)
        
      if sys.argv[2] == "calculateNumberOfSfsVsTurnsBasedOnMaxAmplitudeThreshod":
        from zebrazoom.dataAnalysis.postProcessingFromCommandLine.postProcessingFromCommandLine import calculateNumberOfSfsVsTurnsBasedOnMaxAmplitudeThreshold
        calculateNumberOfSfsVsTurnsBasedOnMaxAmplitudeThreshold(dir_path, sys.argv[3], int(sys.argv[4]))
        
    elif sys.argv[1] == "visualizeMovingAndSleepingTime":
      
      from zebrazoom.code.readValidationVideo import readValidationVideo
      import pandas as pd
      df = pd.read_excel(os.path.join(os.path.join(os.path.join(dir_path, 'ZZoutput'), sys.argv[3]), "sleepVsMoving_" + sys.argv[3] + ".xlsx"))
      nbWells = int(len(df.columns)/3)
      
      if sys.argv[2] == "movingTime":
        
        framesToShow = df[["moving_" + str(i) for i in range(0, nbWells)]].to_numpy()
        readValidationVideo("", sys.argv[3], "", -1, -1, 0, 1, framesToShow)
        
      elif sys.argv[2] == "sleepingTime":
        
        framesToShow = df[["sleep_" + str(i) for i in range(0, nbWells)]].to_numpy()
        readValidationVideo("", sys.argv[3], "", -1, -1, 0, 1, framesToShow)
        
    else:
      
      print("The data produced by ZebraZoom can be found in the folder: " + os.path.join(dir_path,'ZZoutput'))
      pathToVideo = sys.argv[1]
      videoName   = sys.argv[2]
      videoExt    = sys.argv[3]
      configFile  = sys.argv[4]
      argv        = sys.argv
      from zebrazoom.mainZZ import mainZZ
      __spec__ = "ModuleSpec(name='builtins', loader=<class '_frozen_importlib.BuiltinImporter'>)"
      mainZZ(pathToVideo, videoName, videoExt, configFile, argv)
