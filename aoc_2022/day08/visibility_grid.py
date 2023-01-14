from util.grid import Grid
from tree import Tree
from visualisation import prep_point, prep_point_2
from util.visualise_grid import Cell, visualise_grid, update_grid
from time import perf_counter
import cv2
import numpy as np

class VisGrid(Grid):
    def __init__(self, input, cell_info = (11,1,20)):
        super().__init__(input, Tree, point_args=[self])
        self.frames = 0
        self._array = self._build_array()
        self._recording = False
        self._recording_video = False
        self._image = None
        self._file = None
        self._cell_info = cell_info
    
    @property
    def array(self):
        return self._array
    
    def start_recording(self,record_video):
        data = [[prep_point_2(x.height,False,False,None) for x in y] for y in self.array]
        self._image, self._file = visualise_grid(data,*self._cell_info)
        self._file.save('./.output/start.png')
        
        if record_video:
            self._recording_video = True
            first_frame = np.array(self._file)[:,:,::-1]
            width, height, _ = first_frame.shape
            self._video = cv2.VideoWriter('output.avi',cv2.VideoWriter_fourcc(*'MJPG'),60,(width, height))
            self._video.write(first_frame)
        self._recording = True
        
    def stop_recording(self):
        if self._recording_video:
            cv2.destroyAllWindows
            self._video.release()
        self._recording = False
       
    def record_state(self):
        skip_frames = 1
        if self._recording is False:
            return

        if self._recording_video:
            frame = np.array(self._file)[:,:,::-1]
            if self.frames % skip_frames == 0:
                self._video.write(frame)
        else:
            self._file.save(f'./.output/{self.frames:05}.png')
        print(f"Frame {self.frames}", end='\r')
        
        self.frames += 1
        
    def update_cell(self,point):
        if self._recording:
            # t1 = perf_counter()
            cell = prep_point(point)
            # t2 = perf_counter()
            self._image = update_grid(self._image, point.position.x,point.position.y,cell,*self._cell_info)
            # t3 = perf_counter()
            # print(f"Cell updated in {t3-t1} seconds: prep time: {t2-t1}, update time: {t3-t2}")
            

    def count_visible(self):
        return sum(tree.is_visible() for tree in self)

    def highest_vis_score(self):
        return max(tree.calculate_vis_score() for tree in self)