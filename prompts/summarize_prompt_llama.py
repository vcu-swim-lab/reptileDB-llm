step_one = """<s>[INST]<<SYS>> You are tasked with analyzing a text dataset that contains information 
about various reptile families, along with their characteristics and the frequency of each characteristic's 
occurrence. There should be no other information besides the knowledge you're told to give below.

Characteristic Ranking: Rank the characteristics based on their frequency of occurrence in descending order, 
with the most common characteristic labeled as '1', the second most common characteristic labeled as '2', and so on. 
Proceed up to the 30th most common characteristic. Alongside each characteristic should be its number of occurrences. 
For instance, [rank]. [characteristic], [frequency]. Only output the ranked list.
<</SYS>>
"""

step_two = """<s>[INST]<<SYS>>You are tasked with analyzing a text dataset that contains information about reptile 
characteristics and the frequency of each characteristic's occurrence. Your job is to group synonymous 
characteristics or ones that are more detailed versions of others from the text dataset, and update the new counts. 
Create a new ordered list with the updated counts. If you group synonymous characteristics together, remember that 
you need to increment the count. The format should be [rank]. [characteristic], [frequency]. Only output this 
list. Give no fluff and ask no questions.

<s>[INST]
Example 1:
boidae,supralabials,2
boidae,mineralized internarial septum,2
boidae,postorbital and frontal,2
boidae,parietal,2
boidae,frontal,1
boidae,coronoid,2
boidae,lateroventral ledge of the surangular,2
boidae,posterior trunk intercostal arteries,2
boidae,hemipenis,2
boidae,sulcus,2
boidae,rostral,2
boidae,scales above the eye,2
boidae,8 to 11 scales across the forehead,2
boidae,shields between the frontal and large rostral,2
boidae,azygous prefrontal,2
boidae,preocular,2
boidae,supraoculars,2
boidae,post-oculars,2
boidae,temporals,2
boidae,upper labials,2
boidae,lower labials,2
boidae,scale formula,2
boidae,normal scale count,2
boidae,ventrals,2
boidae,subcaudals,2
boidae,sexual dimorphism,2
boidae,coloration,2
boidae,eyes,2[/INST]

Answer:
1. Supralabials, 2
2. Mineralized internarial septum, 2
3. Postorbital and frontal, 2
4. Parietal, 2
5. Frontal, 1
6. Coronoid, 2
7. Lateroventral ledge of the surangular, 2
8. Posterior trunk intercostal arteries, 2
9. Hemipenis, 2
10. Sulcus, 2
11. Rostral, 2
12. Scales above the eye, 2
13. 8 to 11 scales across the forehead, 2
14. Shields between the frontal and large rostral, 2
15. Azygous prefrontal, 2
16. Preocular, 2
17. Supraoculars, 2
18. Post-oculars, 2
19. Temporals, 2
20. Upper labials, 2
21. Lower labials, 2
22. Scale formula, 2
23. Normal scale count, 2
24. Ventrals, 2
25. Subcaudals, 2
26. Sexual dimorphism, 2
27. Coloration, 2
28. Eyes, 2
</s>
<</SYS>>"""