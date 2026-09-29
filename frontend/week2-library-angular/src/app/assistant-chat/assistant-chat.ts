import {
  ChangeDetectorRef,
  Component,
  OnDestroy
} from '@angular/core';

import {
  FormsModule
} from '@angular/forms';

import {
  AuthService
} from '../auth.service';


interface StreamEvent {
  type: string;
  content?: string;
  sources?: string[];
  message?: string;
  completed?: boolean;
}


@Component({
  selector: 'app-assistant-chat',
  standalone: true,

  imports: [
    FormsModule
  ],

  templateUrl:
    './assistant-chat.html',

  styleUrl:
    './assistant-chat.css'
})
export class AssistantChat
  implements OnDestroy {

  question = '';

  answer = '';

  sources: string[] = [];

  errorMessage = '';

  isStreaming = false;

  delayMs = 150;

  private abortController:
    AbortController | null = null;

  private readonly apiUrl =
    'https://localhost:7038/api/assistant/ask/stream';


  constructor(
    private authService: AuthService,
    private changeDetector:
      ChangeDetectorRef
  ) {}


  async askQuestion(): Promise<void> {
    const cleanedQuestion =
      this.question.trim();

    if (!cleanedQuestion) {
      this.errorMessage =
        'Please enter a question.';

      return;
    }

    const token =
      this.authService.getToken();

    if (!token) {
      this.errorMessage =
        'You must be logged in to use the AI assistant.';

      return;
    }

    this.stopStreaming();

    this.answer = '';

    this.sources = [];

    this.errorMessage = '';

    this.isStreaming = true;

    this.abortController =
      new AbortController();

    this.changeDetector
      .detectChanges();

    try {
      const response =
        await fetch(
          this.apiUrl,
          {
            method: 'POST',

            headers: {
              'Content-Type':
                'application/json',

              'Authorization':
                `Bearer ${token}`
            },

            body: JSON.stringify({
              question:
                cleanedQuestion,

              delayMs:
                this.delayMs
            }),

            signal:
              this.abortController
                .signal
          }
        );

      if (!response.ok) {
        const text =
          await response.text();

        throw new Error(
          text ||
          `Request failed with status ${response.status}.`
        );
      }

      if (!response.body) {
        throw new Error(
          'Streaming response body is unavailable.'
        );
      }

      const reader =
        response.body.getReader();

      const decoder =
        new TextDecoder();

      let buffer = '';

      while (true) {
        const {
          value,
          done
        } = await reader.read();

        if (done) {
          break;
        }

        buffer +=
          decoder.decode(
            value,
            {
              stream: true
            }
          );

        buffer =
          this.processBuffer(
            buffer
          );
      }

      if (buffer.trim()) {
        this.processEventBlock(
          buffer
        );
      }

    } catch (error: unknown) {
      if (
        error instanceof DOMException &&
        error.name === 'AbortError'
      ) {
        this.errorMessage =
          'Streaming was cancelled.';
      }
      else {
        this.errorMessage =
          error instanceof Error
            ? error.message
            : 'An unexpected streaming error occurred.';
      }
    }
    finally {
      this.isStreaming = false;

      this.abortController =
        null;

      this.changeDetector
        .detectChanges();
    }
  }


  private processBuffer(
    buffer: string
  ): string {

    let separatorIndex =
      buffer.indexOf('\n\n');

    while (
      separatorIndex !== -1
    ) {
      const eventBlock =
        buffer
          .slice(
            0,
            separatorIndex
          )
          .trim();

      buffer =
        buffer.slice(
          separatorIndex + 2
        );

      if (eventBlock) {
        this.processEventBlock(
          eventBlock
        );
      }

      separatorIndex =
        buffer.indexOf('\n\n');
    }

    return buffer;
  }


  private processEventBlock(
    block: string
  ): void {

    const dataLines =
      block
        .split('\n')
        .filter(
          line =>
            line.startsWith(
              'data:'
            )
        );

    if (
      dataLines.length === 0
    ) {
      return;
    }

    const jsonText =
      dataLines
        .map(
          line =>
            line
              .slice(5)
              .trim()
        )
        .join('');

    try {
      const event =
        JSON.parse(
          jsonText
        ) as StreamEvent;

      this.handleStreamEvent(
        event
      );
    }
    catch {
      this.errorMessage =
        'Received an invalid streaming event.';
    }
  }


  private handleStreamEvent(
    event: StreamEvent
  ): void {

    switch (
      event.type
    ) {
      case 'token':
        if (
          event.content
        ) {
          this.answer +=
            event.content;
        }

        break;

      case 'sources':
        this.sources =
          event.sources ?? [];

        break;

      case 'error':
        this.errorMessage =
          event.message ??
          'The AI service returned an error.';

        break;

      case 'done':
        this.isStreaming =
          false;

        break;
    }

    this.changeDetector
      .detectChanges();
  }


  stopStreaming(): void {
    if (
      this.abortController
    ) {
      this.abortController
        .abort();

      this.abortController =
        null;
    }
  }


  clearChat(): void {
    this.stopStreaming();

    this.question = '';

    this.answer = '';

    this.sources = [];

    this.errorMessage = '';

    this.isStreaming = false;

    this.changeDetector
      .detectChanges();
  }


  ngOnDestroy(): void {
    this.stopStreaming();
  }
}