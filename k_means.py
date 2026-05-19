'''
Final means:
1 : (155.75275884055128, 113.44788856736476, 68.4198832703909) => 20389
2 : (202.10345204282282, 170.10345204282282, 121.78894472361809) => 9154
3 : (114.66537638789855, 75.27880207802791, 39.36121014566568) => 9817
4 : (243.64666359871146, 224.0891854578923, 187.1955821445007) => 10865
'''  
import PIL
from PIL import Image
import urllib.request
import io, sys, os, random

def choose_random_means(k, img, pix):
   m = []
   for _ in range(k):
      x = random.randint(0, img.size[0]-1)
      y = random.randint(0, img.size[1]-1)
      m.append(pix[x, y])
   # if k == 3, return 3 tuples in a list. e.g. [(123, 0, 13), (32, 152, 255), (33, 56, 123)]
   return m

def check_move_count(mc):
   # mc is a list
   # if every single value in mc is 0, return True
   return all(m==0 for m in mc)

def dist(col, m):
   # m is a list of pixels (list of means)
   # return the means bucket index of the minimum distance from the current color
   minIndex = 0
   minDist = float('inf')
   for i, mean in enumerate(m):
      d = sum((col[j]-mean[j])**2 for j in range(3))**0.5
      if d < minDist:
         minDist = d
         minIndex = i
   return minIndex

def clustering(img, pix, cb, mc, m, count):
   tmp_pb = [[] for _ in m]
   tmp_cb = [0 for _ in m]
   tmp_mc = [0 for _ in m]
   tmp_m = [(0, 0, 0) for _ in m]
   for x in range(img.size[0]):
      for y in range(img.size[1]):
         col = pix[x, y]
         index = dist(col, m)
         tmp_pb[index].append((x, y))
         tmp_cb[index] += 1
   new_means = []
   for i in range(len(m)):
      if tmp_cb[i]==0:
         new_means.append(m[i])
         continue
      r_sum = g_sum = b_sum = 0
      for (x, y) in tmp_pb[i]:
         r, g, b = pix[x, y]
         r_sum += r
         g_sum += g
         b_sum += b
      new_mean = (r_sum/tmp_cb[i], g_sum/tmp_cb[i], b_sum/tmp_cb[i])
      tmp_m[i] = new_mean
      tmp_mc[i]=0 if new_mean==m[i] else 1
   return tmp_cb, tmp_mc, tmp_m

def update_picture(img, pix, means):
   region_dict = {}
   for x in range(img.size[0]):
      for y in range(img.size[1]):
         col = pix[x, y]
         index = dist(col, means)
         new_col = tuple(map(int, means[index]))
         pix[x, y] = new_col
         if new_col not in region_dict:
               region_dict[new_col] = []
         region_dict[new_col].append((x, y))
   return pix, region_dict

def distinct_pix_count(img, pix):
   cols = {} # color: count 
   max_col, max_count = pix[0, 0], 0
   for c in range(img.size[0]):
      for r in range(img.size[1]):
         cur_color = pix[c, r]
         if cur_color in cols: 
            cols[cur_color] += 1 
         else: 
            cols[cur_color] = 1 
   max_count = max(cols.values())
   max_color = [key for key in cols if cols[key]==max_count]
   max_col = max_color[0]
   return len(cols.keys()), max_col, max_count

def fill_region_nums(img, pix, means):
   temp_mat = [[0 for _ in range(img.size[1])] for _ in range(img.size[0])]
   for x in range(img.size[0]):
      for y in range(img.size[1]):
         col = pix[x, y]
         i = dist(col, means)
         temp_mat[x][y] = i
   return temp_mat

def BFS(initial_pos, region_dict, color, img):
   visited = {initial_pos}
   frontier = [initial_pos]
   w, h = img.size
   while frontier:
      x, y = frontier.pop(0)
      for dx in [-1, 0, 1]:
         for dy in [-1, 0, 1]:
               nx, ny = x+dx, y+dy
               if (0<=nx<w and 0<=ny<h and (nx, ny) not in visited and (nx, ny) in region_dict[color]):
                  visited.add((nx, ny))
                  frontier.append((nx, ny))
   return visited
   
def count_regions(img, region_dict, pix, means):
   visited_point = set()
   region_count = [0 for _ in means]
   for i, m in enumerate(means):
      color = tuple(map(int, m))
      if color not in region_dict:
         continue
      for p in region_dict[color]:
         if p not in visited_point:
               new_region = BFS(p, region_dict, color, img)
               visited_point |= new_region
               region_count[i] += 1
   return region_count
 
def main():
   k = int(input("k: "))
   file = input("image file: ")
   if not os.path.isfile(file):
      file = os.path.join("/Users/micaylapang/Desktop", file)
   img = Image.open(file)
   img.show()
   pix = img.load() # pix[0, 0] : (r, g, b) 
   c = 0
   for x in range(img.size[0]):
      for y in range(img.size[1]):
         if pix[x, y] == (255, 255, 255):
            c += 1
   print (img.size[0], img.size[1], c)
   print ('Size:', img.size[0], 'x', img.size[1])
   print ('Pixels:', img.size[0]*img.size[1])
   d_count, m_col, m_count = distinct_pix_count(img, pix)
   print ('Distinct pixel count:', d_count)
   print ('Most common pixel:', m_col, '=>', m_count)

   count_buckets = [0 for x in range(k)]
   move_count = [10 for x in range(k)]
   means = choose_random_means(k, img, pix)
   print ('random means:', means)
   count = 1
   while not check_move_count(move_count):
      count += 1
      count_buckets, move_count, means = clustering(img, pix, count_buckets, move_count, means, count)
      if count == 2:
         print ('first means:', means)
         print ('starting sizes:', count_buckets)
   pix, region_dict = update_picture(img, pix, means)
   print ('Final sizes:', count_buckets)
   print ('Final means:')
   for i in range(len(means)):
      print (i+1, ':', means[i], '=>', count_buckets[i])

   img.show()
   
if __name__ == '__main__': 
   main()