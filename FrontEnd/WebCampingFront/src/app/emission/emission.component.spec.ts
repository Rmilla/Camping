import { ComponentFixture, TestBed } from '@angular/core/testing';

import { EmissionComponent } from './emission.component';

describe('EmissionComponent', () => {
  let component: EmissionComponent;
  let fixture: ComponentFixture<EmissionComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [EmissionComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(EmissionComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
