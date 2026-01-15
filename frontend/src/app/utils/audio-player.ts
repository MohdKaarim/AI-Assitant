
/**
 * Helper utility for handling audio playback in the application.
 */

export class AudioPlayer {
    private static currentAudio: HTMLAudioElement | null = null;

    /**
     * Play an audio Blob directly.
     */
    static async playBlob(blob: Blob): Promise<void> {
        const url = URL.createObjectURL(blob);
        await AudioPlayer.playUrl(url);
        URL.revokeObjectURL(url);
    }

    /**
     * Play audio from a URL.
     */
    static playUrl(url: string): Promise<void> {
        this.stop(); // Ensure any previous audio is stopped
        return new Promise((resolve, reject) => {
            this.currentAudio = new Audio(url);

            this.currentAudio.onended = () => {
                this.currentAudio = null;
                resolve();
            };
            this.currentAudio.onerror = (e) => {
                this.currentAudio = null;
                reject(e);
            };

            this.currentAudio.play().catch(reject);
        });
    }

    static pause() {
        if (this.currentAudio) {
            this.currentAudio.pause();
        }
    }

    static resume() {
        if (this.currentAudio) {
            this.currentAudio.play();
        }
    }

    static stop() {
        if (this.currentAudio) {
            this.currentAudio.pause();
            this.currentAudio.currentTime = 0;
            this.currentAudio = null;
        }
    }

    /**
     * Play a specific frequency/tone (useful for feedback beeps).
     */
    static playTone(frequency: number = 440, duration: number = 0.5, type: OscillatorType = 'sine'): void {
        const ctx = new (window.AudioContext || (window as any).webkitAudioContext)();
        const osc = ctx.createOscillator();
        const gain = ctx.createGain();

        osc.type = type;
        osc.frequency.setValueAtTime(frequency, ctx.currentTime);

        gain.gain.setValueAtTime(0.1, ctx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.00001, ctx.currentTime + duration);

        osc.connect(gain);
        gain.connect(ctx.destination);

        osc.start();
        osc.stop(ctx.currentTime + duration);
    }
}
