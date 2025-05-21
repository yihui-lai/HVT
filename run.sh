for mass in 3000; do
for x in {0..19}; do
  echo "$(echo "$x*0.05" | bc -l) $(echo "$x*0.05 + 0.05" | bc -l)"
  python3 steer.py --gfstart=$(echo "$x*0.05" | bc -l) --gfend=$(echo "$x*0.05 + 0.05" | bc -l) --m_values=$mass
done
done





