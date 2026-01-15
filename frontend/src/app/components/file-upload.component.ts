
import { Component, EventEmitter, Output } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ApiService, OCRResponse } from '../services/api.service';

@Component({
  selector: 'app-file-upload',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div class="upload-container glass-panel">
      <h3>1. Upload Text Image</h3>
      
      <div 
        class="drop-zone" 
        [class.dragging]="isDragging"
        (dragover)="onDragOver($event)"
        (dragleave)="onDragLeave($event)"
        (drop)="onDrop($event)"
        (click)="fileInput.click()">
        
        <input 
          #fileInput 
          type="file" 
          (change)="onFileSelected($event)" 
          accept="image/*" 
          hidden>
          
        <div *ngIf="!previewUrl" class="placeholder">
          <p>Drag & Drop or Click to Upload</p>
          <span class="sub-text">Supports PNG, JPG (Eng, Ara, Tam)</span>
        </div>

        <img *ngIf="previewUrl" [src]="previewUrl" class="preview-image" alt="Preview">
      </div>

      <div class="actions" *ngIf="selectedFile">
        <select #langSelect (change)="language = langSelect.value" class="lang-select">
          <option value="eng">English</option>
          <option value="ara">Arabic</option>
          <option value="tam">Tamil</option>
        </select>
        
        <button 
          class="btn-primary" 
          [disabled]="isLoading" 
          (click)="upload()">
          {{ isLoading ? 'Extracting...' : 'Extract Text' }}
        </button>
      </div>

      <div *ngIf="errorMessage" class="error-msg">
        {{ errorMessage }}
      </div>
    </div>
  `,
  styles: [`
    .upload-container {
      padding: 2rem;
      text-align: center;
    }
    .drop-zone {
      border: 2px dashed var(--surface-hover);
      border-radius: var(--radius-md);
      min-height: 200px;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      margin: 1.5rem 0;
      transition: all 0.3s;
      cursor: pointer;
      position: relative;
      overflow: hidden;
    }
    .drop-zone:hover, .drop-zone.dragging {
      border-color: var(--secondary-color);
      background: rgba(30, 41, 59, 0.5);
    }
    .preview-image {
      max-width: 100%;
      max-height: 300px;
      object-fit: contain;
    }
    .placeholder p {
      font-size: 1.1rem;
      font-weight: 600;
      margin-bottom: 0.5rem;
    }
    .sub-text {
      color: var(--text-muted);
      font-size: 0.9rem;
    }
    .actions {
      display: flex;
      gap: 1rem;
      justify-content: center;
      margin-top: 1.5rem;
    }
    .lang-select {
      background: var(--surface-color);
      color: var(--text-main);
      border: 1px solid var(--border-color);
      padding: 0 1rem;
      border-radius: var(--radius-md);
      font-family: inherit;
    }
    .error-msg {
      color: #ef4444;
      margin-top: 1rem;
    }
  `]
})
export class FileUploadComponent {
  @Output() textExtracted = new EventEmitter<string>();

  isDragging = false;
  selectedFile: File | null = null;
  previewUrl: string | null = null;
  isLoading = false;
  language = 'eng';
  errorMessage = '';

  constructor(private api: ApiService) { }

  onDragOver(event: DragEvent) {
    event.preventDefault();
    this.isDragging = true;
  }

  onDragLeave(event: DragEvent) {
    event.preventDefault();
    this.isDragging = false;
  }

  onDrop(event: DragEvent) {
    event.preventDefault();
    this.isDragging = false;
    if (event.dataTransfer?.files.length) {
      this.handleFile(event.dataTransfer.files[0]);
    }
  }

  onFileSelected(event: any) {
    if (event.target.files.length) {
      this.handleFile(event.target.files[0]);
    }
  }

  handleFile(file: File) {
    if (!file.type.startsWith('image/')) {
      this.errorMessage = "Please upload an image file.";
      return;
    }
    this.selectedFile = file;
    this.errorMessage = '';

    const reader = new FileReader();
    reader.onload = () => {
      this.previewUrl = reader.result as string;
    };
    reader.readAsDataURL(file);
  }

  upload() {
    if (!this.selectedFile) return;

    this.isLoading = true;
    this.errorMessage = '';

    this.api.uploadImage(this.selectedFile, this.language).subscribe({
      next: (res) => {
        this.isLoading = false;
        this.textExtracted.emit(res.extracted_text);
      },
      error: (err) => {
        this.isLoading = false;
        this.errorMessage = "Failed to extract text. Please try again.";
        console.error(err);
      }
    });
  }
}
