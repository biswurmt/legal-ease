// WAV encoding utility functions for audio recording

/**
 * Encodes an AudioBuffer to WAV format
 */
export function encodeWAV(audioBuffer: AudioBuffer): Blob {
  const numChannels = audioBuffer.numberOfChannels
  const sampleRate = audioBuffer.sampleRate
  const format = 1 // PCM
  const bitsPerSample = 16

  const samples = interleave(audioBuffer)
  const buffer = new ArrayBuffer(44 + samples.length * 2)
  const view = new DataView(buffer)

  // RIFF chunk descriptor
  writeString(view, 0, "RIFF")
  view.setUint32(4, 36 + samples.length * 2, true)
  writeString(view, 8, "WAVE")

  // fmt subchunk
  writeString(view, 12, "fmt ")
  view.setUint32(16, 16, true) // subchunk1 size
  view.setUint16(20, format, true)
  view.setUint16(22, numChannels, true)
  view.setUint32(24, sampleRate, true)
  view.setUint32(28, (sampleRate * numChannels * bitsPerSample) / 8, true)
  view.setUint16(32, (numChannels * bitsPerSample) / 8, true)
  view.setUint16(34, bitsPerSample, true)

  // data subchunk
  writeString(view, 36, "data")
  view.setUint32(40, samples.length * 2, true)

  // write PCM samples
  let offset = 44
  for (let i = 0; i < samples.length; i++, offset += 2) {
    const s = Math.max(-1, Math.min(1, samples[i]))
    view.setInt16(offset, s < 0 ? s * 0x8000 : s * 0x7fff, true)
  }

  return new Blob([view], { type: "audio/wav" })
}

/**
 * Interleaves audio channels into a single Float32Array
 */
function interleave(buffer: AudioBuffer): Float32Array {
  const numChannels = buffer.numberOfChannels
  const length = buffer.length
  const result = new Float32Array(length * numChannels)

  for (let i = 0; i < length; i++) {
    for (let ch = 0; ch < numChannels; ch++) {
      result[i * numChannels + ch] = buffer.getChannelData(ch)[i]
    }
  }
  return result
}

/**
 * Writes a string to a DataView at the specified offset
 */
function writeString(view: DataView, offset: number, str: string): void {
  for (let i = 0; i < str.length; i++) {
    view.setUint8(offset + i, str.charCodeAt(i))
  }
}
