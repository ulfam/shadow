'use client'

import { useState, useRef, useEffect } from 'react'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Progress } from '@/components/ui/progress'
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card'
import { Play, Download, Upload, Youtube } from 'lucide-react'

interface JobStatus {
  job_id: string
  status: string
  progress: number
  message: string
  error?: string
}

export default function Home() {
  const [youtubeUrl, setYoutubeUrl] = useState('')
  const [repeats, setRepeats] = useState(3)
  const [isProcessing, setIsProcessing] = useState(false)
  const [jobId, setJobId] = useState<string | null>(null)
  const [jobStatus, setJobStatus] = useState<JobStatus | null>(null)
  const [videoUrl, setVideoUrl] = useState<string | null>(null)
  const [uploadedFile, setUploadedFile] = useState<File | null>(null)
  const [useFileUpload, setUseFileUpload] = useState(false)
  const fileInputRef = useRef<HTMLInputElement>(null)
  const videoRef = useRef<HTMLVideoElement>(null)

  // Poll job status
  useEffect(() => {
    if (!jobId || !isProcessing) return

    const pollStatus = async () => {
      try {
        const response = await fetch(`http://localhost:8000/api/status/${jobId}`)
        if (response.ok) {
          const status: JobStatus = await response.json()
          setJobStatus(status)
          
          if (status.status === 'completed') {
            setIsProcessing(false)
            setVideoUrl(`http://localhost:8000/api/download/${jobId}`)
          } else if (status.status === 'error') {
            setIsProcessing(false)
          }
        }
      } catch (error) {
        console.error('Error polling status:', error)
      }
    }

    const interval = setInterval(pollStatus, 2000)
    return () => clearInterval(interval)
  }, [jobId, isProcessing])

  const handleFileUpload = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0]
    if (file) {
      setUploadedFile(file)
      setYoutubeUrl('')
    }
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()


    if (!youtubeUrl && !uploadedFile) {
      alert('Please provide either a YouTube URL or upload a video file.')
      return
    }

    setIsProcessing(true)
    setJobStatus(null)
    setVideoUrl(null)

    try {
      const formData = new FormData()
      formData.append('repeats', repeats.toString())
      
      if (youtubeUrl) {
        formData.append('youtube_url', youtubeUrl)
      } else if (uploadedFile) {
        formData.append('file', uploadedFile)
      }

      const response = await fetch('http://localhost:8000/api/process', {
        method: 'POST',
        body: formData,
      })

      if (response.ok) {
        const result = await response.json()
        setJobId(result.job_id)
      } else {
        const error = await response.text()
        alert(`Error: ${error}`)
        setIsProcessing(false)
      }
    } catch (error) {
      console.error('Error submitting job:', error)
      alert('Error submitting job. Please try again.')
      setIsProcessing(false)
    }
  }

  const handleDownload = () => {
    if (videoUrl) {
      const link = document.createElement('a')
      link.href = videoUrl
      link.download = `shadowing_${jobId}.mp4`
      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-black p-4">
      <div className="max-w-4xl mx-auto">
        <div className="text-center mb-12">
          <h1 className="text-5xl font-bold bg-gradient-to-r from-blue-400 via-purple-500 to-pink-500 bg-clip-text text-transparent mb-6 leading-normal">
              Shadowing UK
            </h1>
          <p className="text-xl text-gray-300 mb-4">
            Create shadowing practice videos from YouTube content
          </p>
          <div className="w-24 h-1 bg-gradient-to-r from-blue-500 to-purple-500 mx-auto rounded-full"></div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Input Form */}
          <Card className="bg-gray-800/50 border-gray-700 backdrop-blur-sm shadow-2xl">
            <CardHeader>
              <CardTitle className="text-2xl text-white flex items-center space-x-2">
                <div className="w-2 h-8 bg-gradient-to-b from-blue-500 to-purple-500 rounded-full"></div>
                <span>Process Video</span>
              </CardTitle>
              <CardDescription className="text-gray-400">
                Enter a YouTube URL or upload a video file to create a shadowing practice video
              </CardDescription>
            </CardHeader>
            <CardContent>
              <form onSubmit={handleSubmit} className="space-y-6">
                {/* Input Method Toggle */}
                <div className="flex space-x-4 p-1 bg-gray-700/50 rounded-lg">
                  <Button
                    type="button"
                    variant={!useFileUpload ? "default" : "ghost"}
                    onClick={() => setUseFileUpload(false)}
                    className={`flex items-center space-x-2 flex-1 ${
                      !useFileUpload 
                        ? "bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-white shadow-lg" 
                        : "text-gray-300 hover:text-white hover:bg-gray-600/50"
                    }`}
                  >
                    <Youtube className="w-4 h-4" />
                    <span>YouTube URL</span>
                  </Button>
                  <Button
                    type="button"
                    variant={useFileUpload ? "default" : "ghost"}
                    onClick={() => setUseFileUpload(true)}
                    className={`flex items-center space-x-2 flex-1 ${
                      useFileUpload 
                        ? "bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-white shadow-lg" 
                        : "text-gray-300 hover:text-white hover:bg-gray-600/50"
                    }`}
                  >
                    <Upload className="w-4 h-4" />
                    <span>Upload File</span>
                  </Button>
                </div>

                {/* YouTube URL Input */}
                {!useFileUpload && (
                  <div className="space-y-2">
                    <Label htmlFor="youtube-url" className="text-gray-300 font-medium">YouTube URL</Label>
                    <Input
                      id="youtube-url"
                      type="url"
                      placeholder="https://www.youtube.com/watch?v=..."
                      value={youtubeUrl}
                      onChange={(e) => setYoutubeUrl(e.target.value)}
                      disabled={isProcessing}
                      className="bg-gray-700/50 border-gray-600 text-white placeholder-gray-400 focus:border-blue-500 focus:ring-blue-500/20"
                    />
                  </div>
                )}

                {/* File Upload */}
                {useFileUpload && (
                  <div className="space-y-2">
                    <Label htmlFor="file-upload" className="text-gray-300 font-medium">Video File (MP4, max 15 min)</Label>
                    <Input
                      id="file-upload"
                      type="file"
                      accept="video/mp4,video/*"
                      onChange={handleFileUpload}
                      disabled={isProcessing}
                      ref={fileInputRef}
                      className="bg-gray-700/50 border-gray-600 text-white file:bg-gray-600 file:border-gray-500 file:text-white file:rounded file:px-4 file:py-2 file:mr-4"
                    />
                    {uploadedFile && (
                      <p className="text-sm text-gray-400">
                        Selected: {uploadedFile.name}
                      </p>
                    )}
                  </div>
                )}

                {/* Repeats */}
                <div className="space-y-2">
                  <Label htmlFor="repeats" className="text-gray-300 font-medium">Number of Repeats</Label>
                  <Input
                    id="repeats"
                    type="number"
                    min="1"
                    max="10"
                    value={repeats}
                    onChange={(e) => setRepeats(parseInt(e.target.value) || 3)}
                    disabled={isProcessing}
                    className="bg-gray-700/50 border-gray-600 text-white focus:border-blue-500 focus:ring-blue-500/20"
                  />
                </div>

                {/* Submit Button */}
                <Button
                  type="submit"
                  disabled={isProcessing || (!youtubeUrl && !uploadedFile)}
                  className="w-full bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-white font-semibold py-3 rounded-lg shadow-lg transform transition-all duration-200 hover:scale-105 disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none"
                >
                  {isProcessing ? (
                    <div className="flex items-center space-x-2">
                      <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                      <span>Processing...</span>
                    </div>
                  ) : (
                    <div className="flex items-center space-x-2">
                      <Play className="w-4 h-4" />
                      <span>Start Processing</span>
                    </div>
                  )}
                </Button>
                </form>
                </CardContent>
                </Card>


          {/* Status and Video Player */}
          <div className="space-y-6">
            {/* Status Card */}
            {jobStatus && (
              <Card className="bg-gray-800/50 border-gray-700 backdrop-blur-sm shadow-2xl">
                <CardHeader>
                  <CardTitle className="text-xl text-white flex items-center space-x-2">
                    <div className="w-2 h-6 bg-gradient-to-b from-green-500 to-blue-500 rounded-full"></div>
                    <span>Processing Status</span>
                  </CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="flex justify-between items-center">
                    <span className="text-gray-300">Status:</span>
                    <span className={`px-3 py-1 rounded-full text-sm font-medium ${
                      jobStatus.status === 'completed' 
                        ? 'bg-green-500/20 text-green-400 border border-green-500/30'
                        : jobStatus.status === 'error'
                        ? 'bg-red-500/20 text-red-400 border border-red-500/30'
                        : 'bg-blue-500/20 text-blue-400 border border-blue-500/30'
                    }`}>
                      {jobStatus.status}
                    </span>
                  </div>
                  
                  {jobStatus.progress > 0 && (
                    <div className="space-y-2">
                      <div className="flex justify-between text-sm">
                        <span className="text-gray-300">Progress</span>
                        <span className="text-gray-400">{jobStatus.progress}%</span>
                      </div>
                      <Progress 
                        value={jobStatus.progress} 
                        className="h-2 bg-gray-700"
                      />
                    </div>
                  )}
                  
                  {jobStatus.message && (
                    <p className="text-gray-400 text-sm">{jobStatus.message}</p>
                  )}
                  
                  {jobStatus.error && (
                    <p className="text-red-400 text-sm bg-red-500/10 p-3 rounded-lg border border-red-500/20">
                      {jobStatus.error}
                    </p>
                  )}
                </CardContent>
              </Card>
            )}

            {/* Video Player */}
            {videoUrl && (
              <Card className="bg-gray-800/50 border-gray-700 backdrop-blur-sm shadow-2xl">
                <CardHeader>
                  <CardTitle className="text-xl text-white flex items-center space-x-2">
                    <div className="w-2 h-6 bg-gradient-to-b from-purple-500 to-pink-500 rounded-full"></div>
                    <span>Your Shadowing Video</span>
                  </CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="relative">
                    <video
                      ref={videoRef}
                      controls
                      className="w-full rounded-lg shadow-lg"
                      style={{ maxHeight: '400px' }}
                    >
                      <source src={videoUrl} type="video/mp4" />
                      Your browser does not support the video tag.
                    </video>
                  </div>
                  
                  <Button
                    onClick={handleDownload}
                    className="w-full bg-gradient-to-r from-green-600 to-blue-600 hover:from-green-700 hover:to-blue-700 text-white font-semibold py-3 rounded-lg shadow-lg transform transition-all duration-200 hover:scale-105"
                  >
                    <Download className="w-4 h-4 mr-2" />
                    Download Video
                  </Button>
                </CardContent>
              </Card>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}