/**
 * Tests for audio encoding utilities.
 * These tests ensure WAV encoding logic remains correct during refactoring.
 */
import { describe, it, expect, beforeEach } from 'vitest'

// We'll extract these functions during refactoring, but test them in-place first
// Copy the functions from case.tsx for testing
function encodeWAV(audioBuffer: AudioBuffer) {
  const numChannels = audioBuffer.numberOfChannels;
  const sampleRate = audioBuffer.sampleRate;
  const format = 1; // PCM
  const bitsPerSample = 16;

  const samples = interleave(audioBuffer);
  const buffer = new ArrayBuffer(44 + samples.length * 2);
  const view = new DataView(buffer);

  // RIFF chunk descriptor
  writeString(view, 0, "RIFF");
  view.setUint32(4, 36 + samples.length * 2, true);
  writeString(view, 8, "WAVE");

  // fmt subchunk
  writeString(view, 12, "fmt ");
  view.setUint32(16, 16, true);
  view.setUint16(20, format, true);
  view.setUint16(22, numChannels, true);
  view.setUint32(24, sampleRate, true);
  view.setUint32(28, sampleRate * numChannels * bitsPerSample / 8, true);
  view.setUint16(32, numChannels * bitsPerSample / 8, true);
  view.setUint16(34, bitsPerSample, true);

  // data subchunk
  writeString(view, 36, "data");
  view.setUint32(40, samples.length * 2, true);

  // write PCM samples
  let offset = 44;
  for (let i = 0; i < samples.length; i++, offset += 2) {
    let s = Math.max(-1, Math.min(1, samples[i]));
    view.setInt16(offset, s < 0 ? s * 0x8000 : s * 0x7fff, true);
  }

  return new Blob([view], { type: "audio/wav" });
}

function interleave(buffer: AudioBuffer) {
  const numChannels = buffer.numberOfChannels;
  const length = buffer.length;
  const result = new Float32Array(length * numChannels);

  for (let i = 0; i < length; i++) {
    for (let ch = 0; ch < numChannels; ch++) {
      result[i * numChannels + ch] = buffer.getChannelData(ch)[i];
    }
  }
  return result;
}

function writeString(view: DataView, offset: number, str: string) {
  for (let i = 0; i < str.length; i++) {
    view.setUint8(offset + i, str.charCodeAt(i));
  }
}

// Mock AudioBuffer for testing
class MockAudioBuffer {
  numberOfChannels: number
  sampleRate: number
  length: number
  private channelData: Float32Array[]

  constructor(options: { numberOfChannels: number; sampleRate: number; length: number }) {
    this.numberOfChannels = options.numberOfChannels
    this.sampleRate = options.sampleRate
    this.length = options.length
    this.channelData = Array.from(
      { length: options.numberOfChannels },
      () => new Float32Array(options.length)
    )
  }

  getChannelData(channel: number): Float32Array {
    return this.channelData[channel]
  }
}

describe('Audio Encoding Utilities', () => {
  describe('writeString', () => {
    it('should write string to DataView at correct offset', () => {
      const buffer = new ArrayBuffer(10)
      const view = new DataView(buffer)

      writeString(view, 0, 'RIFF')

      expect(view.getUint8(0)).toBe('R'.charCodeAt(0))
      expect(view.getUint8(1)).toBe('I'.charCodeAt(0))
      expect(view.getUint8(2)).toBe('F'.charCodeAt(0))
      expect(view.getUint8(3)).toBe('F'.charCodeAt(0))
    })
  })

  describe('interleave', () => {
    it('should interleave mono audio correctly', () => {
      const mockBuffer = new MockAudioBuffer({
        numberOfChannels: 1,
        sampleRate: 44100,
        length: 4
      })

      const channelData = mockBuffer.getChannelData(0)
      channelData[0] = 0.5
      channelData[1] = -0.5
      channelData[2] = 0.25
      channelData[3] = -0.25

      const result = interleave(mockBuffer as unknown as AudioBuffer)

      expect(result.length).toBe(4)
      expect(result[0]).toBe(0.5)
      expect(result[1]).toBe(-0.5)
      expect(result[2]).toBe(0.25)
      expect(result[3]).toBe(-0.25)
    })

    it('should interleave stereo audio correctly', () => {
      const mockBuffer = new MockAudioBuffer({
        numberOfChannels: 2,
        sampleRate: 44100,
        length: 2
      })

      // Left channel
      const leftChannel = mockBuffer.getChannelData(0)
      leftChannel[0] = 1.0
      leftChannel[1] = 0.5

      // Right channel
      const rightChannel = mockBuffer.getChannelData(1)
      rightChannel[0] = -1.0
      rightChannel[1] = -0.5

      const result = interleave(mockBuffer as unknown as AudioBuffer)

      // Interleaved: L0, R0, L1, R1
      expect(result.length).toBe(4)
      expect(result[0]).toBe(1.0)   // Left sample 0
      expect(result[1]).toBe(-1.0)  // Right sample 0
      expect(result[2]).toBe(0.5)   // Left sample 1
      expect(result[3]).toBe(-0.5)  // Right sample 1
    })
  })

  describe('encodeWAV', () => {
    it('should create valid WAV blob with correct type', () => {
      const mockBuffer = new MockAudioBuffer({
        numberOfChannels: 1,
        sampleRate: 44100,
        length: 100
      })

      const blob = encodeWAV(mockBuffer as unknown as AudioBuffer)

      expect(blob.type).toBe('audio/wav')
    })

    it('should have correct file size for mono audio', () => {
      const length = 100
      const numChannels = 1
      const mockBuffer = new MockAudioBuffer({
        numberOfChannels: numChannels,
        sampleRate: 44100,
        length: length
      })

      const blob = encodeWAV(mockBuffer as unknown as AudioBuffer)

      // WAV file size = 44 bytes (header) + (samples * channels * 2 bytes per sample)
      const expectedSize = 44 + (length * numChannels * 2)
      expect(blob.size).toBe(expectedSize)
    })

    it('should have correct file size for stereo audio', () => {
      const length = 100
      const numChannels = 2
      const mockBuffer = new MockAudioBuffer({
        numberOfChannels: numChannels,
        sampleRate: 44100,
        length: length
      })

      const blob = encodeWAV(mockBuffer as unknown as AudioBuffer)

      // WAV file size = 44 bytes (header) + (samples * channels * 2 bytes per sample)
      const expectedSize = 44 + (length * numChannels * 2)
      expect(blob.size).toBe(expectedSize)
    })

    it('should handle different sample rates', () => {
      const mockBuffer1 = new MockAudioBuffer({
        numberOfChannels: 1,
        sampleRate: 44100,
        length: 100
      })

      const mockBuffer2 = new MockAudioBuffer({
        numberOfChannels: 1,
        sampleRate: 48000,
        length: 100
      })

      const blob1 = encodeWAV(mockBuffer1 as unknown as AudioBuffer)
      const blob2 = encodeWAV(mockBuffer2 as unknown as AudioBuffer)

      // Both should create valid blobs
      expect(blob1.type).toBe('audio/wav')
      expect(blob2.type).toBe('audio/wav')
      // File sizes should be the same (sample rate affects header only)
      expect(blob1.size).toBe(blob2.size)
    })

    it('should handle empty audio buffer', () => {
      const mockBuffer = new MockAudioBuffer({
        numberOfChannels: 1,
        sampleRate: 44100,
        length: 0
      })

      const blob = encodeWAV(mockBuffer as unknown as AudioBuffer)

      // Should still create a valid WAV with just header
      expect(blob.type).toBe('audio/wav')
      expect(blob.size).toBe(44) // Just the header
    })
  })
})
