import json
import numpy as np
import pandas as pd
import os
import time
import datetime

def calculateSleepVsMovingPeriods(pathToZZoutput, vidName, speedThresholdForMoving, notMovingNumberOfFramesThresholdForSleep, specifiedStartTime=0, distanceTravelledRollingMedianFilter=0, videoPixelSize=-1, videoFPS=-1):
  
  videoNamelist    = []
  dfFinalAllVideos = pd.DataFrame()
  currentNbFrames  = 0
  
  if ',' in vidName:
    videoNamelist = vidName.split(',')
  else:
    videoNamelist = [vidName]
  
  for idx, videoName in enumerate(videoNamelist):
  
    pathToVideo = os.path.join(pathToZZoutput, videoName, "results_" + videoName + ".txt")
    
    with open(pathToVideo) as ff:
      dataRef = json.load(ff)
    
    if videoPixelSize == -1:
      if "videoPixelSize" in dataRef:
        videoPixelSize = dataRef["videoPixelSize"]
      else:
        print("You should add the parameter 'videoPixelSize' in your configuration file")
        videoPixelSize = 1
    
    if videoFPS == -1:
      if "videoFPS" in dataRef:
        videoFPS = dataRef["videoFPS"]
      else:
        print("You should add the parameter 'videoFPS' in your configuration file")
        videoFPS = 1
    
    if idx == 0 and type(specifiedStartTime) == str and len(specifiedStartTime) > 1:
      t = datetime.datetime.strptime(specifiedStartTime, "%H:%M:%S")
      currentNbFrames = (t.hour * 60 * 60 + t.minute * 60 + t.second) * videoFPS
    
    dfFinal = pd.DataFrame()
    totalFrames  = len(dataRef['wellPoissMouv'][0][0][0]["HeadX"])
    times = [time.strftime('%H:%M:%S', time.gmtime(second)) for second in [(i + currentNbFrames) / videoFPS for i in range(0, totalFrames + 1)]]
    currentNbFrames = currentNbFrames + totalFrames + 1
    df = pd.DataFrame(data = np.transpose([times]), columns = ['HourMinuteSecond'])
    dfFinal = pd.concat([dfFinal, df], axis=1)
    
    for wellNumber in range(len(dataRef['wellPoissMouv'])):
      
      displacementVector = videoPixelSize * np.diff(np.array([dataRef['wellPoissMouv'][wellNumber][0][0]["HeadX"], dataRef['wellPoissMouv'][wellNumber][0][0]["HeadY"]]))
      squaredDisplacement = displacementVector * displacementVector
      distance = np.sqrt(squaredDisplacement[0] + squaredDisplacement[1])
      # distance = np.append(distance, [0])
      distance = np.insert(distance, 0, 0)
      distance = np.insert(distance, 0, 0)
      if distanceTravelledRollingMedianFilter:
        distance2 = np.convolve(distance, np.ones(distanceTravelledRollingMedianFilter), 'same') / distanceTravelledRollingMedianFilter
        distance2[:distanceTravelledRollingMedianFilter-1] = distance[:distanceTravelledRollingMedianFilter-1]
        distance2[-distanceTravelledRollingMedianFilter+1:] = distance[-distanceTravelledRollingMedianFilter+1:]
        distance = distance2
      
      speed = distance * videoFPS
      
      moving = speed > speedThresholdForMoving
      
      sleep = np.array([False for i in range(len(moving))])
      countNotMovingFrames = 0
      for i in range(len(sleep)):
        if moving[i]:
          countNotMovingFrames = 0
        else:
          countNotMovingFrames = countNotMovingFrames + 1
          if countNotMovingFrames >= notMovingNumberOfFramesThresholdForSleep:
            sleep[i] = True
          if countNotMovingFrames == notMovingNumberOfFramesThresholdForSleep:
            countNotMovingFrames2 = countNotMovingFrames - 1
            j = i - 1
            while j >= 0 and countNotMovingFrames2 > 0:
              sleep[j] = True
              countNotMovingFrames2 = countNotMovingFrames2 - 1
              j = j - 1
      
      df = pd.DataFrame(data = np.transpose(np.append(np.append([speed], [moving], axis=0), [sleep], axis=0)), columns = ['speed_' + str(wellNumber), 'moving_' + str(wellNumber), 'sleep_' + str(wellNumber)])
      dfFinal = pd.concat([dfFinal, df], axis=1)
    
    dfFinal.to_excel(os.path.join(pathToZZoutput, videoName, "sleepVsMoving_" + videoName + ".xlsx"))
    dfFinalAllVideos = pd.concat([dfFinalAllVideos, dfFinal], axis=0)
    
    
  if len(videoNamelist) > 1:
    
    concatExcelFileName = "".join(videoNamelist)
    dfFinalAllVideos.to_excel(os.path.join(pathToZZoutput, "sleepVsMoving_" + concatExcelFileName + ".xlsx"))

def firstSleepingTimeAfterSpecifiedTime(pathToZZoutput, vidName, specifiedTime, wellNumber):
  
  videoNamelist    = []
  if ',' in vidName:
    concatExcelFileName = "".join(vidName.split(','))
    df = pd.read_excel(os.path.join(pathToZZoutput, "sleepVsMoving_" + concatExcelFileName + ".xlsx"))
  else:
    df = pd.read_excel(os.path.join(os.path.join(pathToZZoutput, vidName), "sleepVsMoving_" + vidName + ".xlsx"))
  
  dfTimeMinusSpecifiedTime = (df['HourMinuteSecond'].apply(datetime.datetime.strptime, args=("%H:%M:%S",)) - datetime.datetime.strptime(specifiedTime, "%H:%M:%S")).apply(pd.Timedelta.total_seconds).apply(abs)
  indexStart = dfTimeMinusSpecifiedTime.argmin()
  dfLength = len(df)
  
  if int(wellNumber) == -1:
    allWellNumbers = [str(i) for i in range(0, int(len(df.columns) / 3))]
  else:
    allWellNumbers = [wellNumber]
  
  for wellNum in allWellNumbers:
    currentIndex = indexStart
    while (currentIndex != dfLength) and (df['sleep_' + wellNum][currentIndex] == 0):
      currentIndex = currentIndex + 1
    if currentIndex == dfLength:
      print("For the well number", wellNum, ", couldn't find any time point after", specifiedTime, "for which the fish was sleeping")
    else:
      print("For the well number:", wellNum, "and the specified time:", specifiedTime, ".")
      print("The first time after the specified time when the fish starts sleeping is at", df['HourMinuteSecond'][currentIndex], "(which corresponds to frame number:", currentIndex, ").")
      print("In other words, the fish starts sleeping", dfTimeMinusSpecifiedTime[currentIndex], "seconds after the specified time (or", currentIndex - indexStart, "frames after the specified time) (or", time.strftime('%H:%M:%S', time.gmtime(dfTimeMinusSpecifiedTime[currentIndex])), "Hours:Minutes:Seconds after the specified time)")

def numberOfSleepingAndMovingTimesInTimeRange(pathToZZoutput, vidName, specifiedStartTime, specifiedEndTime, wellNumber):
  
  videoNamelist    = []
  if ',' in vidName:
    concatExcelFileName = "".join(vidName.split(','))
    df = pd.read_excel(os.path.join(pathToZZoutput, "sleepVsMoving_" + concatExcelFileName + ".xlsx"))
  else:
    df = pd.read_excel(os.path.join(os.path.join(pathToZZoutput, vidName), "sleepVsMoving_" + vidName + ".xlsx"))
  
  dfTimeMinusSpecifiedStartTime = (df['HourMinuteSecond'].apply(datetime.datetime.strptime, args=("%H:%M:%S",)) - datetime.datetime.strptime(specifiedStartTime, "%H:%M:%S")).apply(pd.Timedelta.total_seconds).apply(abs)
  indexStart = dfTimeMinusSpecifiedStartTime.argmin()
  
  dfTimeMinusSpecifiedEndTime = (df['HourMinuteSecond'].apply(datetime.datetime.strptime, args=("%H:%M:%S",)) - datetime.datetime.strptime(specifiedEndTime, "%H:%M:%S")).apply(pd.Timedelta.total_seconds).apply(abs)
  indexEnd = dfTimeMinusSpecifiedEndTime.argmin()
  
  dfLength = len(df)
  
  if int(wellNumber) == -1:
    allWellNumbers = [str(i) for i in range(0, int(len(df.columns) / 3))]
  else:
    allWellNumbers = [wellNumber]
  
  print("Between time", specifiedStartTime, "(frame number", indexStart, "), and time:", specifiedEndTime, "(frame number", indexEnd,"):")
  
  for wellNum in allWellNumbers:
  
    print("For well number", wellNum, ":")
    
    nbSleepFrames  = np.sum(df['sleep_'  + wellNum][indexStart:indexEnd])
    nbMovingFrames = np.sum(df['moving_' + wellNum][indexStart:indexEnd])
    
    print(nbSleepFrames, "sleeping Frames")
    print(nbMovingFrames, "moving frames\n")
    